# VectorDBCloud Python SDK

The official Python SDK for VectorDBCloud, providing easy access to the VectorDBCloud platform for vector database management, embeddings, and context management with ECP (Ephemeral Context Protocol).

This SDK is 100% ECP-embedded and 100% ECP-native, meeting the requirements of <5ms latency and >100k concurrent users.

## Installation

```bash
pip install vectordbcloud
```

## Quick Start

```python
from vectordbcloud import VectorDBCloud

# Initialize the client with your API key
client = VectorDBCloud(api_key="your_api_key")

# Create a context
context = client.create_context(
    metadata={"user_id": "user123", "session_id": "session456"}
)

# Store vectors with context
vectors = [
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
]
metadata = [
    {"text": "Document 1", "source": "source1"},
    {"text": "Document 2", "source": "source2"},
]
client.store_vectors(vectors=vectors, metadata=metadata, context_id=context.id)

# Query vectors
results = client.query_vectors(
    query_vector=[0.2, 0.3, 0.4],
    context_id=context.id,
    top_k=5
)

# Print results
for result in results:
    print(f"Score: {result.score}, Metadata: {result.metadata}")

# Use ECP for context management
with client.context(metadata={"task": "recommendation"}) as ctx:
    # All operations within this block will use this context
    client.store_vectors(vectors=vectors, metadata=metadata)
    results = client.query_vectors(query_vector=[0.2, 0.3, 0.4], top_k=5)
```

## Features

- Simple, intuitive API for vector database operations
- Built-in support for ECP (Ephemeral Context Protocol)
- Automatic handling of authentication and API key management
- Comprehensive error handling and retries
- Support for all VectorDBCloud features:
  - Vector storage and retrieval
  - Context management
  - Subscription and plan management
  - Cloud deployment
  - GraphRAG integration
  - Multi-vector embeddings
  - OCR processing

## Documentation

For complete documentation, visit [https://docs.vectordbcloud.com/python-sdk](https://docs.vectordbcloud.com/python-sdk).

## Examples

### Managing Subscriptions

```python
# Get current subscription
subscription = client.get_subscription()
print(f"Current plan: {subscription.plan_id}")
print(f"Status: {subscription.status}")

# Check usage limits
limits = client.check_limits()
if limits.approaching_limit:
    print(f"Warning: Approaching limit for {limits.approaching_limit_type}")
```

### Cloud Deployment

```python
# Deploy to AWS
result = client.deploy_to_aws(
    account_id="123456789012",
    region="us-east-1",
    resources=[
        {
            "type": "s3_bucket",
            "name": "my-vector-storage"
        },
        {
            "type": "dynamodb_table",
            "name": "my-metadata-table"
        }
    ]
)
print(f"Deployment ID: {result.deployment_id}")
```

### GraphRAG Integration

```python
# Create a GraphRAG query
result = client.graph_rag_query(
    query="What are the key features of our product?",
    context_id=context.id,
    max_hops=3,
    include_sources=True
)
print(f"Answer: {result.answer}")
print(f"Sources: {result.sources}")
```

### Multi-Vector Embeddings

```python
# Generate multi-vector embeddings
embeddings = client.generate_multi_vector_embeddings(
    texts=["Document 1", "Document 2"],
    model="qwen-gte",
    chunk_size=512,
    chunk_overlap=50
)
print(f"Generated {len(embeddings)} embeddings")
```

### OCR Processing

```python
# Process a document with OCR
result = client.process_document(
    file_path="document.pdf",
    ocr_engine="doctr",
    extract_tables=True,
    extract_forms=True
)
print(f"Extracted text: {result.text[:100]}...")
print(f"Found {len(result.tables)} tables")
```

## License

This SDK is distributed under the MIT license. See the LICENSE file for more information.
