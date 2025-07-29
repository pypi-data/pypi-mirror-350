"""Snowflake vector store implementation for LangChain."""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class SnowflakeVectorStore(VectorStore):
    """Snowflake vector store implementation.
    
    This class provides a vector store implementation using Snowflake's
    vector data type and similarity search capabilities.
    """

    def __init__(
        self,
        account: str,
        user: str,
        password: str,
        database: str,
        schema: str,
        warehouse: str,
        role: str,
        table_name: str,
        embedding_function: Optional[Embeddings] = None,
        embedding_dimension: int = 1536,
        **kwargs: Any,
    ) -> None:
        """Initialize the Snowflake vector store.
        
        Args:
            account: Snowflake account identifier
            user: Snowflake username
            password: Snowflake password
            database: Snowflake database name
            schema: Snowflake schema name
            warehouse: Snowflake warehouse name
            role: Snowflake role name
            table_name: Name of the table to store vectors
            embedding_function: Function to generate embeddings
            embedding_dimension: Dimension of the embedding vectors
            **kwargs: Additional arguments
        """
        self.account = account
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema
        self.warehouse = warehouse
        self.role = role
        self.table_name = table_name
        self.embedding_function = embedding_function
        self.embedding_dimension = embedding_dimension

        # Create connection string
        connection_string = (
            f"snowflake://{user}:{password}@{account}/{database}/{schema}"
            f"?warehouse={warehouse}&role={role}"
        )
        
        self.engine = create_engine(connection_string, **kwargs)
        self._init_table()

    def _init_table(self) -> None:
        """Initialize the vector store table."""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text(
                        f"""
                        CREATE TABLE IF NOT EXISTS {self.table_name} (
                            id VARCHAR PRIMARY KEY,
                            content VARCHAR,
                            metadata VARCHAR,
                            embedding VECTOR(FLOAT, {self.embedding_dimension})
                        )
                        """
                    )
                )
                conn.commit()
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to initialize table: {str(e)}")

    def recreate_table(self) -> None:
        """Drop and recreate the table with the correct schema."""
        try:
            with self.engine.connect() as conn:
                # Drop the existing table
                conn.execute(text(f"DROP TABLE IF EXISTS {self.table_name}"))
                # Create the table with the correct schema
                conn.execute(
                    text(
                        f"""
                        CREATE TABLE {self.table_name} (
                            id VARCHAR PRIMARY KEY,
                            content VARCHAR,
                            metadata VARCHAR,
                            embedding VECTOR(FLOAT, {self.embedding_dimension})
                        )
                        """
                    )
                )
                conn.commit()
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to recreate table: {str(e)}")
            
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Add texts to the vector store.
        
        Args:
            texts: List of texts to add
            metadatas: Optional list of metadata dictionaries
            **kwargs: Additional arguments to pass to the embedding function
            
        Returns:
            List of document IDs
            
        Raises:
            ValueError: If embedding_function is not set
            SQLAlchemyError: If there's an error adding texts
        """
        if not self.embedding_function:
            raise ValueError("embedding_function must be set to add texts")
            
        if not metadatas:
            metadatas = [{} for _ in texts]
            
        try:
            embeddings = self.embedding_function.embed_documents(texts)
            ids = [str(uuid4()) for _ in texts]
            
            with self.engine.connect() as conn:
                for text_content, metadata, embedding, doc_id in zip(texts, metadatas, embeddings, ids):
                    # First, insert the row without the embedding
                    conn.execute(
                        text(f"""
                            INSERT INTO {self.table_name} (id, content, metadata)
                            VALUES (:id, :content, :metadata)
                        """),
                        {
                            "id": doc_id,
                            "content": text_content,
                            "metadata": json.dumps(metadata),
                        }
                    )
                    
                    # Then, update the row with the embedding using the correct VECTOR syntax
                    embedding_array = '[' + ','.join(map(str, embedding)) + ']'
                    conn.execute(
                        text(f"""
                            UPDATE {self.table_name} 
                            SET embedding = {embedding_array}::VECTOR(FLOAT, {self.embedding_dimension})
                            WHERE id = :id
                        """),
                        {"id": doc_id}
                    )
                conn.commit()
            return ids
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to add texts: {str(e)}")
            
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Search for similar documents.
        
        Args:
            query: Query text
            k: Number of results to return
            filter: Optional metadata filter
            **kwargs: Additional arguments to pass to the embedding function
            
        Returns:
            List of documents most similar to the query
            
        Raises:
            ValueError: If embedding_function is not set
            SQLAlchemyError: If there's an error searching
        """
        if not self.embedding_function:
            raise ValueError("embedding_function must be set to search")
            
        try:
            query_embedding = self.embedding_function.embed_query(query)
            # Format embedding as array string for Snowflake VECTOR type
            embedding_array = '[' + ','.join(map(str, query_embedding)) + ']'
            
            # Build WHERE clause for metadata filtering
            where_clause = ""
            filter_params = {"k": k}
            
            if filter:
                conditions = []
                for key, value in filter.items():
                    param_name = f"filter_{key}"
                    # Use JSON_EXTRACT_PATH_TEXT for filtering instead of PARSE_JSON
                    conditions.append(f"JSON_EXTRACT_PATH_TEXT(metadata, '{key}') = :{param_name}")
                    filter_params[param_name] = str(value)
                where_clause = "WHERE " + " AND ".join(conditions)
            
            with self.engine.connect() as conn:
                sql_query = f"""
                        SELECT content, metadata
                        FROM {self.table_name}
                        {where_clause}
                        ORDER BY VECTOR_COSINE_SIMILARITY(embedding, {embedding_array}::VECTOR(FLOAT, {self.embedding_dimension})) DESC
                        LIMIT :k
                        """
                
                results = conn.execute(
                    text(sql_query),
                    filter_params,
                ).fetchall()
                
            return [
                Document(page_content=content, metadata=json.loads(metadata) if metadata else {})
                for content, metadata in results
            ]
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to search: {str(e)}")
            
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        """Search for similar documents with scores.
        
        Args:
            query: Query text
            k: Number of results to return
            **kwargs: Additional arguments to pass to the embedding function
            
        Returns:
            List of tuples containing documents and their similarity scores
            
        Raises:
            ValueError: If embedding_function is not set
            SQLAlchemyError: If there's an error searching
        """
        if not self.embedding_function:
            raise ValueError("embedding_function must be set to search")
            
        try:
            query_embedding = self.embedding_function.embed_query(query)
            # Format embedding as array string for Snowflake VECTOR type
            embedding_array = '[' + ','.join(map(str, query_embedding)) + ']'
            
            with self.engine.connect() as conn:
                results = conn.execute(
                    text(
                        f"""
                        SELECT content, metadata, VECTOR_COSINE_SIMILARITY(embedding, {embedding_array}::VECTOR(FLOAT, {self.embedding_dimension})) as score
                        FROM {self.table_name}
                        ORDER BY score DESC
                        LIMIT :k
                        """
                    ),
                    {"k": k},
                ).fetchall()
                
            return [
                (Document(page_content=content, metadata=json.loads(metadata) if metadata else {}), score)
                for content, metadata, score in results
            ]
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to search with score: {str(e)}")
            
    def similarity_search_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        **kwargs: Any,
    ) -> List[Document]:
        """Search for similar documents by embedding vector.
        
        Args:
            embedding: Query embedding vector
            k: Number of results to return
            **kwargs: Additional arguments
            
        Returns:
            List of documents most similar to the query embedding
            
        Raises:
            SQLAlchemyError: If there's an error searching
        """
        try:
            # Format embedding as array string for Snowflake VECTOR type
            embedding_array = '[' + ','.join(map(str, embedding)) + ']'
            
            with self.engine.connect() as conn:
                results = conn.execute(
                    text(
                        f"""
                        SELECT content, metadata
                        FROM {self.table_name}
                        ORDER BY VECTOR_COSINE_SIMILARITY(embedding, {embedding_array}::VECTOR(FLOAT, {self.embedding_dimension})) DESC
                        LIMIT :k
                        """
                    ),
                    {"k": k},
                ).fetchall()
                
            return [
                Document(page_content=content, metadata=json.loads(metadata) if metadata else {})
                for content, metadata in results
            ]
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to search by vector: {str(e)}")

    def delete(self, ids: Optional[List[str]] = None, **kwargs: Any) -> Optional[bool]:
        """Delete documents from the vector store.
        
        Args:
            ids: List of document IDs to delete
            **kwargs: Additional arguments
            
        Returns:
            True if deletion was successful, False otherwise
        """
        if not ids:
            return True
            
        try:
            with self.engine.connect() as conn:
                for doc_id in ids:
                    delete_stmt = text(f"DELETE FROM {self.table_name} WHERE id = :id")
                    conn.execute(delete_stmt, {"id": doc_id})
                conn.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting documents: {e}")
            return False

    def get_by_ids(self, ids: List[str]) -> List[Document]:
        """Get documents by their IDs.
        
        Args:
            ids: List of document IDs
            
        Returns:
            List of documents
        """
        try:
            with self.engine.connect() as conn:
                documents = []
                for doc_id in ids:
                    result = conn.execute(
                        text(f"SELECT content, metadata FROM {self.table_name} WHERE id = :id"),
                        {"id": doc_id}
                    ).fetchone()
                    
                    if result:
                        content, metadata_str = result
                        metadata = json.loads(metadata_str) if metadata_str else {}
                        doc = Document(page_content=content, metadata=metadata)
                        documents.append(doc)
                        
            return documents
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving documents: {e}")
            return []

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> "SnowflakeVectorStore":
        """Create a vector store from texts.
        
        Args:
            texts: List of texts to add
            embedding: Embedding function
            metadatas: Optional list of metadata dictionaries
            **kwargs: Additional arguments for the vector store
            
        Returns:
            SnowflakeVectorStore instance
        """
        vector_store = cls(embedding_function=embedding, **kwargs)
        vector_store.add_texts(texts, metadatas)
        return vector_store

    def delete_table(self) -> None:
        """Delete the entire table.
        
        This method is primarily used for cleanup in tests.
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {self.table_name}"))
                conn.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting table: {e}")
            raise 