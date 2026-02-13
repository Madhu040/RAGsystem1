# Healthcare AI RAG System

A complete Retrieval-Augmented Generation (RAG) system for healthcare AI documents using OpenAI embeddings and ChromaDB.

## 📊 Project Status

✅ **OPERATIONAL** - 208 documents embedded and ready to query

### Current Setup:
- **Documents**: 4 healthcare AI sources loaded
- **Chunks**: 208 text chunks (500 chars each, 100 overlap)
- **Embeddings**: text-embedding-3-large (3072 dimensions)
- **Vector DB**: ChromaDB (4.8 MB)
- **Collection**: `healthcare_ai_500_large`

---

## 📁 Project Structure

```
WEEK2-POC/
├── .env                      # OpenAI API key
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── rag_pipeline.py           # ✨ Main RAG system (load, chunk, embed, store)
├── query_system.py           # 🔍 Query interface for ChromaDB
│
├── chroma_db/                # ChromaDB vector database (4.8 MB)
├── embeddings_backup.pkl     # Backup of embeddings
├── venv_py312/               # Python 3.12 virtual environment
│
└── SETUP/                    # Installation guides and verification scripts
    ├── install_homebrew_python.sh
    ├── install_chromadb_env.sh
    ├── FIX_BREW_NOT_FOUND.md
    ├── PYTHON_312_INSTALL_GUIDE.md
    ├── SETUP_SUMMARY.md
    ├── verify_chromadb.py
    └── [other setup files]
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12 (see `SETUP/` for installation guides)
- OpenAI API key in `.env` file

### Setup (if not already done)

```bash
# 1. Activate virtual environment
source venv_py312/bin/activate

# 2. Verify ChromaDB
python SETUP/verify_chromadb.py
```

### Usage

#### Option 1: Use Existing Data (Recommended)
Your embeddings are already loaded! Just query:

```bash
source venv_py312/bin/activate
python query_system.py
```

#### Option 2: Rebuild from Scratch

```bash
source venv_py312/bin/activate
python rag_pipeline.py
```

---

## 💻 Usage Examples

### Query the System

```python
from query_system import query_chromadb

# Ask a question
results = query_chromadb(
    "What is Elevance Health's AI strategy?",
    n_results=5
)
```

### Using the Full Pipeline

```python
from rag_pipeline import RAGSystem

# Initialize
rag = RAGSystem(chunk_size=500, chunk_overlap=100)

# Load documents
urls = ["https://example.com/article"]
documents = rag.load_documents_from_urls(urls)

# Create chunks
chunks = rag.create_chunks(documents)

# Store in ChromaDB
collection = rag.store_in_chromadb(chunks, "my_collection")

# Query
results = rag.query("my_collection", "your question", n_results=5)
```

---

## 📚 Data Sources

1. **Becker's Payer Issues** - 14 payer AI moves in 2025
2. **Deloitte** - 2026 Global Healthcare Outlook
3. **Fierce Healthcare** - Elevance Health's AI Strategy
4. **NORC Research** - AI in Utilization Management

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### RAG System Settings
```python
# In rag_pipeline.py
chunk_size = 500        # Size of text chunks
chunk_overlap = 100     # Overlap between chunks
embedding_model = "text-embedding-3-large"  # OpenAI model
```

---

## 📖 Example Queries

Try these questions with the query system:

1. "What is Elevance Health's AI strategy?"
2. "How are payers using AI in 2025?"
3. "What are the workforce challenges in healthcare?"
4. "How is AI being used in utilization management?"
5. "What are the cybersecurity concerns for health systems?"

---

## 🛠️ Troubleshooting

### Virtual Environment Not Working
```bash
# Recreate environment
python3.12 -m venv venv_py312
source venv_py312/bin/activate
pip install -r requirements.txt
```

### ChromaDB Errors
```bash
# Verify installation
python SETUP/verify_chromadb.py

# If empty, rebuild
python rag_pipeline.py
```

### "brew: command not found"
See `SETUP/FIX_BREW_NOT_FOUND.md`

### Python 3.14 Compatibility Issues
See `SETUP/PYTHON_312_INSTALL_GUIDE.md`

---

## 📊 Performance

- **Embedding Creation**: ~2.6 seconds for 208 chunks
- **Query Time**: ~100-200ms per query
- **Database Size**: 4.8 MB
- **Cost**: ~$0.00157 for initial embedding

---

## 🔐 Security

- ✅ API keys stored in `.env` (not committed to git)
- ✅ `.gitignore` configured for sensitive files
- ✅ Local vector database (no data sent except to OpenAI for embeddings)

---

## 📝 Development

### Adding New Documents

```python
from rag_pipeline import RAGSystem

rag = RAGSystem()

# Load from URL
docs = rag.load_documents_from_urls(["https://example.com"])

# Or add custom content
doc = rag.add_document(
    content="Your text here",
    metadata={"source": "example", "title": "Example Doc"}
)

# Process and store
chunks = rag.create_chunks([doc])
rag.store_in_chromadb(chunks)
```

### Changing Chunk Size

Edit `rag_pipeline.py`:
```python
rag = RAGSystem(
    chunk_size=1000,      # Larger chunks
    chunk_overlap=200     # More overlap
)
```

---

## 📦 Dependencies

See `requirements.txt` for full list. Key packages:
- `chromadb` - Vector database
- `langchain-openai` - OpenAI integration
- `langchain-community` - Document loaders
- `langchain-text-splitters` - Text chunking
- `python-dotenv` - Environment variables

---

## 🆘 Support

For setup issues, check the `SETUP/` folder:
- `FIX_BREW_NOT_FOUND.md` - Homebrew installation
- `PYTHON_312_INSTALL_GUIDE.md` - Python 3.12 setup
- `SETUP_SUMMARY.md` - Complete setup guide
- `verify_chromadb.py` - Verify your installation

---

## 📄 License

This project is for educational purposes.

---

## 🎯 Next Steps

1. ✅ Documents loaded
2. ✅ Embeddings created
3. ✅ ChromaDB populated
4. 🚀 **Ready to query!**

Run `python query_system.py` to start!
