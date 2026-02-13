#!/usr/bin/env python3
"""
Verify ChromaDB installation and check if embeddings are loaded
"""

import sys
import os

# Activate the venv environment
venv_path = './venv_py312'
if os.path.exists(venv_path):
    activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
    # Python 3.12 venv doesn't have activate_this.py, so we'll use subprocess
    pass

try:
    import chromadb
    from chromadb.config import Settings
    
    print("="*70)
    print(" ChromaDB Installation Verification")
    print("="*70)
    print()
    
    print(f"✅ ChromaDB installed: version {chromadb.__version__}")
    print()
    
    # Connect to the database
    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    print("✅ Connected to ChromaDB at ./chroma_db")
    print()
    
    # List collections
    print("Checking collections...")
    collections = client.list_collections()
    
    if len(collections) == 0:
        print("⚠️  No collections found in ChromaDB")
        print()
        print("Your embeddings are saved in: embeddings_data.pkl")
        print("But they haven't been loaded to ChromaDB yet.")
        print()
        print("To load them, run:")
        print("  source venv_py312/bin/activate")
        print("  python load_to_chromadb.py")
    else:
        print(f"✅ Found {len(collections)} collection(s):")
        print()
        
        for collection in collections:
            print(f"  📦 Collection: {collection.name}")
            count = collection.count()
            print(f"     • Documents: {count}")
            
            if count > 0:
                # Get a sample
                results = collection.peek(limit=1)
                if results and results['documents']:
                    doc_preview = results['documents'][0][:100]
                    print(f"     • Sample: {doc_preview}...")
                    
                # Get metadata
                metadata = collection.metadata
                if metadata:
                    print(f"     • Metadata: {metadata}")
            print()
        
        print("="*70)
        print("✅ EMBEDDINGS ARE LOADED IN CHROMADB!")
        print("="*70)
        print()
        print(f"Total documents: {sum(c.count() for c in collections)}")
        print()
        
except ImportError as e:
    print("❌ ChromaDB is not installed")
    print(f"   Error: {e}")
    print()
    print("Install it with:")
    print("  source venv_py312/bin/activate")
    print("  pip install chromadb")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Try running:")
    print("  source venv_py312/bin/activate")
    print("  python load_to_chromadb.py")
