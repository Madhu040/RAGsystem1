#!/usr/bin/env python3
"""
Check if Python 3.12 is available and help set up ChromaDB environment
"""

import sys
import subprocess
import os

print("="*70)
print(" Python Version Checker for ChromaDB")
print("="*70)
print()

# Check current Python version
current_version = sys.version_info
print(f"Current Python: {current_version.major}.{current_version.minor}.{current_version.micro}")

if current_version.major == 3 and 11 <= current_version.minor <= 12:
    print("✅ This Python version is compatible with ChromaDB!")
    print()
    
    # Try to import chromadb
    try:
        import chromadb
        print(f"✅ ChromaDB is installed (version {chromadb.__version__})")
        print()
        print("You can run: python load_to_chromadb.py")
    except ImportError:
        print("⚠️  ChromaDB not installed yet")
        print()
        print("Install it with:")
        print("  pip install chromadb langchain-community langchain-openai")
    
else:
    print("❌ This Python version is NOT compatible with ChromaDB")
    print()
    print("ChromaDB requires Python 3.11 or 3.12")
    print()
    
    # Check for python3.12
    print("Checking for Python 3.12...")
    try:
        result = subprocess.run(['python3.12', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Found: {result.stdout.strip()}")
            print()
            print("Create a virtual environment:")
            print("  python3.12 -m venv venv_py312")
            print("  source venv_py312/bin/activate")
            print("  pip install chromadb langchain-community langchain-openai")
        else:
            print("❌ Python 3.12 not found")
            print()
            print("Install Python 3.12:")
            print("  brew install python@3.12")
    except FileNotFoundError:
        print("❌ Python 3.12 not found")
        print()
        print("Install Python 3.12:")
        print("  brew install python@3.12")
        print()
        print("Or download from: https://www.python.org/downloads/")

print()
print("="*70)
print(" Next Steps")
print("="*70)
print()

if current_version.major == 3 and 11 <= current_version.minor <= 12:
    print("1. Install packages: pip install chromadb langchain-community langchain-openai")
    print("2. Load embeddings: python load_to_chromadb.py")
    print("3. Start building your RAG system!")
else:
    print("1. Install Python 3.12: brew install python@3.12")
    print("2. Create virtual environment: python3.12 -m venv venv_py312")
    print("3. Activate: source venv_py312/bin/activate")
    print("4. Install packages: pip install chromadb langchain-community langchain-openai")
    print("5. Load embeddings: python load_to_chromadb.py")

print()
