import argparse
import json
import os
from .db import VectorDB

def main():
    parser = argparse.ArgumentParser(description="Vector Database Operations with Qdrant")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Initialize command
    init_parser = subparsers.add_parser("init", help="Initialize vector database")
    init_parser.add_argument("--model", default="all-MiniLM-L6-v2", help="Embedding model name")
    init_parser.add_argument("--collection", default="documents", help="Collection name")
    init_parser.add_argument("--qdrant-url", help="Qdrant server URL (for cloud)")
    init_parser.add_argument("--qdrant-key", help="Qdrant API key (for cloud)")
    init_parser.add_argument("--qdrant-path", help="Path for local Qdrant database")
    
    # Process documents command
    process_parser = subparsers.add_parser("process", help="Process documents into vector database")
    process_parser.add_argument("--input", required=True, help="JSON file with documents {name: text}")
    process_parser.add_argument("--collection", default="documents", help="Collection name")
    process_parser.add_argument("--chunk-size", type=int, default=200, help="Chunk size in words")
    process_parser.add_argument("--overlap", type=int, default=50, help="Overlap between chunks")
    process_parser.add_argument("--qdrant-url", help="Qdrant server URL (for cloud)")
    process_parser.add_argument("--qdrant-key", help="Qdrant API key (for cloud)")
    process_parser.add_argument("--qdrant-path", help="Path for local Qdrant database")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search relevant chunks for query")
    search_parser.add_argument("--query", required=True, help="Query text")
    search_parser.add_argument("--collection", default="documents", help="Collection name")
    search_parser.add_argument("--k", type=int, default=5, help="Number of results to return")
    search_parser.add_argument("--output", help="Output file for results (default: print to console)")
    search_parser.add_argument("--qdrant-url", help="Qdrant server URL (for cloud)")
    search_parser.add_argument("--qdrant-key", help="Qdrant API key (for cloud)")
    search_parser.add_argument("--qdrant-path", help="Path for local Qdrant database")
    
    args = parser.parse_args()
    
    # Common parameters for VectorDB initialization
    db_params = {
        "collection_name": args.collection if hasattr(args, 'collection') else "documents",
        "qdrant_url": args.qdrant_url if hasattr(args, 'qdrant_url') else None,
        "qdrant_api_key": args.qdrant_key if hasattr(args, 'qdrant_key') else None,
        "qdrant_path": args.qdrant_path if hasattr(args, 'qdrant_path') else None,
    }
    
    if args.command == "init":
        db_params["model_name"] = args.model
        db = VectorDB(**db_params)
        print(f"Vector database initialized with model {args.model}")
    
    elif args.command == "process":
        db = VectorDB(**db_params)
        with open(args.input, 'r') as f:
            documents = json.load(f)
        db.add_documents(documents, args.chunk_size, args.overlap)
    
    elif args.command == "search":
        db = VectorDB(**db_params)
        results = db.search(args.query, args.k)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
        else:
            print(json.dumps(results, indent=2))
    
    else:
        parser.print_help()