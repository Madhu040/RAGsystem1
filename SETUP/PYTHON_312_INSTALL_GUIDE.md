# 🔧 Python 3.12 Installation Guide for ChromaDB

## Current Situation
- You have: **Python 3.14**
- ChromaDB needs: **Python 3.11 or 3.12**
- Issue: Python 3.14 is not compatible with ChromaDB 1.5.0

---

## ✅ Solution: Install Python 3.12

### Option 1: Using Homebrew (Recommended)

#### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python 3.12
```bash
brew install python@3.12
```

#### Step 3: Verify Installation
```bash
python3.12 --version
# Should show: Python 3.12.x
```

#### Step 4: Create Virtual Environment
```bash
cd /Users/madhu/Downloads/Cursor_all/AI-ENG-Boot-CAMP/WEEK2-POC

# Create virtual environment with Python 3.12
python3.12 -m venv venv_py312

# Activate it
source venv_py312/bin/activate

# Verify you're using Python 3.12
python --version
```

#### Step 5: Install Packages
```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install chromadb langchain langchain-community langchain-openai \
            langchain-text-splitters python-dotenv beautifulsoup4 requests
```

#### Step 6: Load Embeddings to ChromaDB
```bash
# Make sure venv is activated
source venv_py312/bin/activate

# Run the ChromaDB loader
python load_to_chromadb.py
```

---

### Option 2: Using Python.org Installer

1. Go to https://www.python.org/downloads/
2. Download Python 3.12.x for macOS
3. Run the installer
4. After installation, follow steps 4-6 above using `python3.12`

---

### Option 3: Using pyenv (Advanced)

```bash
# Install pyenv
brew install pyenv

# Install Python 3.12
pyenv install 3.12.0

# Set as local version for this project
cd /Users/madhu/Downloads/Cursor_all/AI-ENG-Boot-CAMP/WEEK2-POC
pyenv local 3.12.0

# Create virtual environment
python -m venv venv_py312
source venv_py312/bin/activate

# Install packages
pip install chromadb langchain langchain-community langchain-openai \
            langchain-text-splitters python-dotenv beautifulsoup4 requests
```

---

## 🚀 Quick Start Commands (Copy & Paste)

Once Homebrew is installed, run these commands:

```bash
# Navigate to your project
cd /Users/madhu/Downloads/Cursor_all/AI-ENG-Boot-CAMP/WEEK2-POC

# Install Python 3.12
brew install python@3.12

# Create virtual environment
python3.12 -m venv venv_py312

# Activate virtual environment
source venv_py312/bin/activate

# Install packages
pip install --upgrade pip
pip install chromadb langchain langchain-community langchain-openai langchain-text-splitters python-dotenv beautifulsoup4 requests

# Load your embeddings into ChromaDB
python load_to_chromadb.py

# When you're done
deactivate
```

---

## 📝 Using the Virtual Environment

### Every time you want to work on this project:

```bash
cd /Users/madhu/Downloads/Cursor_all/AI-ENG-Boot-CAMP/WEEK2-POC
source venv_py312/bin/activate

# Now you can run Python scripts with ChromaDB
python load_to_chromadb.py

# When done
deactivate
```

---

## ✅ What Happens After Setup

Once you complete the setup:

1. ✅ Python 3.12 will be installed
2. ✅ Virtual environment `venv_py312` will be created
3. ✅ ChromaDB will work perfectly
4. ✅ Your 208 embeddings from `embeddings_data.pkl` will load into ChromaDB
5. ✅ You'll have a fully working RAG system!

---

## 🎯 Next Steps After Installation

1. **Load embeddings to ChromaDB:**
   ```bash
   source venv_py312/bin/activate
   python load_to_chromadb.py
   ```

2. **Your embeddings are ready!**
   - 208 chunks
   - text-embedding-3-large (3072 dimensions)
   - Stored in ChromaDB
   - Ready for similarity search

3. **Build your RAG chain and start querying!**

---

## ❓ Troubleshooting

### "Homebrew not found"
- Install Homebrew first using the command in Option 1, Step 1

### "python3.12: command not found"
- Make sure Python 3.12 installed successfully: `brew list python@3.12`
- Try the full path: `/opt/homebrew/bin/python3.12` (Apple Silicon) or `/usr/local/bin/python3.12` (Intel)

### "Module not found"
- Make sure virtual environment is activated: `source venv_py312/bin/activate`
- Reinstall packages: `pip install chromadb langchain-community langchain-openai`

---

## 💡 Alternative: If You Don't Want to Install Python 3.12

You can use **FAISS** instead of ChromaDB (works with Python 3.14):

```bash
pip3 install faiss-cpu
python3 create_embeddings_faiss.py
```

FAISS is actually faster than ChromaDB and works great for RAG!

---

**Choose your path:**
- ✅ **Recommended**: Install Python 3.12 + use ChromaDB
- ✅ **Faster**: Use FAISS with your current Python 3.14

Let me know which approach you'd like to take!
