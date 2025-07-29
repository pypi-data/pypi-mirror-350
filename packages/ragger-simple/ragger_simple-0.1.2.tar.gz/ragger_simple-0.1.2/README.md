# Ragger Simple

A simple Python package for vector database operations using Qdrant.

## Features

- Initialize connection with Qdrant vector database
- Parse, chunk, and process text into vector embeddings
- Search for relevant text chunks based on semantic similarity

## Installation

```bash
pip install ragger-simple
```

## Usage

### Python API

Import and initialize `VectorDB`:

```python
from ragger_simple import VectorDB

db = VectorDB(
    collection_name="my_documents",
    model_name="all-MiniLM-L6-v2",
    model_path=None,
    qdrant_url=None,
    qdrant_api_key=None,
    qdrant_path=None,
    qdrant_timeout=500.0,
)
```

Constructor parameters:

- `collection_name` (str, default: `"documents"`) — Qdrant collection name  
- `model_name` (str, default: `"all-MiniLM-L6-v2"`) — sentence-transformers model  
- `model_path` (str, optional) — local folder with your model  
- `qdrant_url` (str, optional) — cloud URL  
- `qdrant_api_key` (str, optional) — cloud API key  
- `qdrant_path` (str, optional) — local path  
- `qdrant_timeout` (float, default: `500`) — request timeout in seconds

Methods:

```python
db.add_documents(
    documents: Dict[str, str],
    chunk_size: int = 200,
    overlap: int = 50,
)
```

- `documents` — dict mapping doc names to text  
- `chunk_size` — words per chunk  
- `overlap` — overlapping words

```python
results = db.search(
    query: str,
    k: int = 5,
) -> List[Dict]
```

- `query` — query text  
- `k` — number of results

Example:

```python
documents = {
    "Article 1": "This is the content of article 1...",
    "Article 2": "This is the content of article 2..."
}
db.add_documents(documents, chunk_size=200, overlap=50)
results = db.search("your query here", k=5)
print(results)
```

## License

MIT
