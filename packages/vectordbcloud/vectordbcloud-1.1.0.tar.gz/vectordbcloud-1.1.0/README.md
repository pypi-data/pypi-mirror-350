# VectorDBCloud Python SDK

Official Python SDK for VectorDBCloud API.

## Installation

```bash
pip install vectordbcloud
```

## Quick Start

```python
from vectordbcloud import VectorDBCloud

# Initialize client
client = VectorDBCloud(
    api_key="your-api-key",
    base_url="https://api.vectordbcloud.com/prod"  # Optional, defaults to production
)

# Check API health
health = client.health()
print(health)

# Generate embeddings
embedding = client.generate_embedding("Hello, world!")
print(embedding)

# Search vectors
results = client.search_vector(
    vector=[0.1, 0.2, 0.3, 0.4, 0.5],
    limit=10
)
print(results)

# Connect to vector databases
weaviate_config = {
    "url": "http://localhost:8080",
    "api_key": "your-weaviate-key"
}
connection = client.connect_weaviate(weaviate_config)
```

## API Reference

### Core Methods
- `health()` - Check API health
- `version()` - Get API version

### Authentication
- `login(email, password)` - User login
- `logout()` - User logout

### Vector Search
- `search_vector(vector, limit, filters)` - Vector similarity search
- `search_semantic(text, limit, filters)` - Semantic text search

### AI Methods
- `generate_embedding(text)` - Generate text embeddings
- `generate_text(prompt, **kwargs)` - Generate text with AI

### Billing
- `get_usage()` - Get usage statistics
- `get_invoices()` - Get billing invoices

### Vector Database Connections
- `connect_weaviate(config)` - Connect to Weaviate
- `connect_pinecone(config)` - Connect to Pinecone
- `connect_chroma(config)` - Connect to ChromaDB
- `connect_qdrant(config)` - Connect to Qdrant
- `connect_milvus(config)` - Connect to Milvus

## Configuration

```python
client = VectorDBCloud(
    api_key="your-api-key",
    base_url="https://api.vectordbcloud.com/prod",
    timeout=30
)
```

## Error Handling

```python
from vectordbcloud import VectorDBCloud, AuthenticationError, APIError

try:
    client = VectorDBCloud(api_key="invalid-key")
    result = client.health()
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(f"API error: {e}")
```

## Version

Current version: 1.1.0

## License

MIT License

## Support

- Documentation: https://docs.vectordbcloud.com
- GitHub: https://github.com/VectorDBCloud/python-sdk
- Issues: https://github.com/VectorDBCloud/python-sdk/issues
