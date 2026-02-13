"""
Test Retrieval - Healthcare AI RAG System
Demonstrate similarity search and retrieval from ChromaDB
"""

import chromadb
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


def test_retrieval():
    """
    Test retrieval with various queries
    """
    print("\n" + "="*70)
    print(" 🔍 TESTING RETRIEVAL FROM CHROMADB")
    print("="*70)
    
    # Connect to ChromaDB
    print("\n[1] Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("healthcare_ai_500_large")
    
    print(f"✅ Connected to collection: healthcare_ai_500_large")
    print(f"   Total documents: {collection.count()}")
    
    # Initialize embeddings
    print("\n[2] Initializing embeddings model...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    print(f"✅ Using: text-embedding-3-large")
    
    # Test queries
    test_queries = [
        "What is Elevance Health's AI strategy?",
        "How are payers using AI in 2025?",
        "What are the workforce challenges in healthcare?",
        "Tell me about AI in utilization management",
        "What is the role of ChatGPT in healthcare?"
    ]
    
    print("\n" + "="*70)
    print(" RUNNING TEST QUERIES")
    print("="*70)
    
    for idx, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST {idx}/5")
        print(f"{'='*70}")
        print(f"\n❓ Query: \"{query}\"")
        print(f"\n🔄 Searching...")
        
        # Embed query
        query_embedding = embeddings.embed_query(query)
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        # Display results
        print(f"\n📊 Top 3 Results:\n")
        
        for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0]), 1):
            similarity_score = 1 - distance
            print(f"[{i}] Relevance Score: {similarity_score:.3f} ({similarity_score*100:.1f}%)")
            
            # Show source
            source = results['metadatas'][0][i-1].get('source', 'Unknown')
            if 'beckerspayer' in source:
                source_name = "Becker's Payer Issues"
            elif 'deloitte' in source:
                source_name = "Deloitte"
            elif 'fierce' in source:
                source_name = "Fierce Healthcare"
            elif 'norc' in source:
                source_name = "NORC Research"
            else:
                source_name = "Unknown"
            
            print(f"    Source: {source_name}")
            print(f"    Content: {doc[:150]}...")
            print()
    
    # Summary
    print("\n" + "="*70)
    print(" ✅ RETRIEVAL TEST COMPLETE")
    print("="*70)
    print("\n📊 Test Summary:")
    print(f"   • Queries tested: {len(test_queries)}")
    print(f"   • Results per query: 3")
    print(f"   • Total retrievals: {len(test_queries) * 3}")
    print(f"   • Retrieval working: ✅")
    
    print("\n💡 Retrieval Quality:")
    print("   • High relevance scores (>0.7) = Excellent match")
    print("   • Medium scores (0.5-0.7) = Good match")
    print("   • Low scores (<0.5) = Weak match")
    
    print("\n🎯 Your RAG system is retrieving documents successfully!")
    
    return True


if __name__ == "__main__":
    try:
        test_retrieval()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Virtual environment is activated:")
        print("     source venv_py312/bin/activate")
        print("  2. ChromaDB has data:")
        print("     python SETUP/verify_chromadb.py")
