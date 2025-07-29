# LangChain Snowflake Vector Store

A LangChain integration for Snowflake's vector database capabilities, enabling semantic search and similarity matching using Snowflake's native `VECTOR` data type and `VECTOR_COSINE_SIMILARITY` function.

## Features

- 🏔️ **Native Snowflake Integration**: Uses Snowflake's built-in vector capabilities
- 🔍 **Semantic Search**: Powered by `VECTOR_COSINE_SIMILARITY` function
- 📊 **Scalable**: Leverages Snowflake's cloud-native architecture
- 🔒 **Secure**: Enterprise-grade security and compliance
- 🚀 **High Performance**: Optimized for large-scale vector operations

## Installation

```bash
pip install langchain-snowflake-vectorstore
```

## Quick Start

```python
from langchain_snowflake_vectorstore import SnowflakeVectorStore
from langchain_openai import OpenAIEmbeddings

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Create vector store
vector_store = SnowflakeVectorStore(
    account="your-account",
    user="your-username", 
    password="your-password",
    database="your-database",
    schema="your-schema",
    warehouse="your-warehouse",
    role="your-role",
    table_name="vector_documents",
    embedding_function=embeddings,
    embedding_dimension=1536
)

# Add documents
texts = [
    "LangChain is a framework for developing applications powered by language models.",
    "Snowflake is a cloud-based data warehousing platform.",
    "Vector databases enable semantic search and similarity matching."
]

ids = vector_store.add_texts(texts)

# Search for similar documents
results = vector_store.similarity_search("What is LangChain?", k=2)
for doc in results:
    print(doc.page_content)
```

## Configuration

### Environment Variables

You can set your Snowflake credentials using environment variables:

```bash
export SNOWFLAKE_ACCOUNT=your-account
export SNOWFLAKE_USER=your-username
export SNOWFLAKE_PASSWORD=your-password
export SNOWFLAKE_DATABASE=your-database
export SNOWFLAKE_SCHEMA=your-schema
export SNOWFLAKE_WAREHOUSE=your-warehouse
export SNOWFLAKE_ROLE=your-role
```

### Connection Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `account` | Snowflake account identifier | Yes |
| `user` | Username for authentication | Yes |
| `password` | Password for authentication | Yes |
| `database` | Database name | Yes |
| `schema` | Schema name | Yes |
| `warehouse` | Warehouse name | Yes |
| `role` | Role name | No |
| `table_name` | Table name for storing vectors | Yes |
| `embedding_function` | Function to generate embeddings | Yes |
| `embedding_dimension` | Dimension of embedding vectors | Yes |

## Advanced Usage

### Custom Table Creation

```python
# Recreate table with custom settings
vector_store.recreate_table()
```

### Similarity Search with Scores

```python
# Get similarity scores along with documents
results_with_scores = vector_store.similarity_search_with_score("query", k=5)
for doc, score in results_with_scores:
    print(f"Score: {score}, Content: {doc.page_content}")
```

### Adding Documents with Metadata

```python
texts = ["Document 1", "Document 2"]
metadatas = [{"source": "file1.txt"}, {"source": "file2.txt"}]
ids = vector_store.add_texts(texts, metadatas=metadatas)
```

### Batch Operations

```python
# Create from texts (class method)
vector_store = SnowflakeVectorStore.from_texts(
    texts=texts,
    embedding=embeddings,
    account="your-account",
    # ... other parameters
)
```

## Requirements

- Python 3.8+
- Snowflake account with vector support
- LangChain Core
- Snowflake Connector for Python
- SQLAlchemy

## Snowflake Setup

Your Snowflake account must support the `VECTOR` data type and `VECTOR_COSINE_SIMILARITY` function. These features are available in recent Snowflake versions.

### Required Permissions

Ensure your Snowflake role has the following permissions:
- `CREATE TABLE` on the target schema
- `INSERT`, `SELECT`, `UPDATE`, `DELETE` on the vector table
- `USAGE` on the database, schema, and warehouse

## Testing

Run the test suite:

```bash
# Unit tests
pytest tests/test_vectorstore.py

# Integration tests (requires Snowflake credentials)
export SNOWFLAKE_ACCOUNT=your-account
# ... set other environment variables
pytest tests/test_integration.py -m integration
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/your-username/langchain-snowflake-vectorstore/issues)
- LangChain Community: [Join the discussion](https://github.com/langchain-ai/langchain/discussions)

## Changelog

### v0.1.0
- Initial release
- Basic vector store functionality
- Snowflake integration with VECTOR data type
- Similarity search using VECTOR_COSINE_SIMILARITY
- Comprehensive test suite 