"""
Query Interface for Healthcare AI RAG System
Simple script to query your ChromaDB collection
"""

import chromadb
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


def query_chromadb(query_text, collection_name="healthcare_ai_500_large", n_results=5):
    """
    Query the ChromaDB collection
    
    Args:
        query_text: Your question
        collection_name: Collection name (default: healthcare_ai_500_large)
        n_results: Number of results to return (default: 5)
    """
    print(f"\n🔍 Query: {query_text}")
    print("="*70)
    
    # Connect to ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(collection_name)
    
    # Create embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Embed query
    query_embedding = embeddings.embed_query(query_text)
    
    # Query collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Display results
    print(f"\n📊 Found {len(results['documents'][0])} relevant chunks:\n")
    
    for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0]), 1):
        print(f"[{i}] Relevance: {1 - distance:.3f}")
        print(f"    {doc[:200]}...")
        print()
    
    return results


def main():
    """
    Interactive query interface
    """
    print("="*70)
    print(" Healthcare AI Knowledge Base - Query Interface")
    print("="*70)
    print()
    print("Collection: healthcare_ai_500_large")
    print("Documents: 208 chunks")
    print("Model: text-embedding-3-large (3072 dimensions)")
    print()
    print("="*70)
    
    # Example queries
    example_queries = [
        "What is Elevance Health's AI strategy?",
        "How are payers using AI in 2025?",
        "What are the workforce challenges in healthcare?",
        "How is AI being used in utilization management?",
        "What are the cybersecurity concerns for health systems?",
    ]
    
    print("\n📚 Example Queries:")
    for i, q in enumerate(example_queries, 1):
        print(f"  {i}. {q}")
    
    print("\n" + "="*70)
    
    # Interactive mode
    while True:
        print("\nEnter your question (or 'quit' to exit, 'examples' to see list):")
        query = input("> ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if query.lower() == 'examples':
            for i, q in enumerate(example_queries, 1):
                print(f"  {i}. {q}")
            continue
        
        if query.lower().startswith('ex') and query[2:].isdigit():
            # User typed "ex1", "ex2", etc.
            idx = int(query[2:]) - 1
            if 0 <= idx < len(example_queries):
                query = example_queries[idx]
            else:
                print("Invalid example number")
                continue
        
        if not query:
            continue
        
        try:
            results = query_chromadb(query)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nMake sure:")
            print("  1. Virtual environment is activated: source venv_py312/bin/activate")
            print("  2. ChromaDB has data: python rag_pipeline.py")


if __name__ == "__main__":
    main()
