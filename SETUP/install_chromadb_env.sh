#!/bin/bash

# Install ChromaDB Environment with Python 3.12
# Run this AFTER Python 3.12 is installed

echo "========================================================================"
echo " Setting Up ChromaDB Environment"
echo "========================================================================"
echo ""

# Check if python3.12 is available
if ! command -v python3.12 &> /dev/null; then
    echo "❌ python3.12 not found"
    echo ""
    echo "Please install Python 3.12 first:"
    echo "  ./install_homebrew_python.sh"
    exit 1
fi

PYTHON_VERSION=$(python3.12 --version)
echo "✅ Found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment with Python 3.12..."
python3.12 -m venv venv_py312

if [ $? -eq 0 ]; then
    echo "✅ Virtual environment created: venv_py312"
else
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv_py312/bin/activate

# Verify we're in the right environment
VENV_PYTHON=$(python --version)
echo "✓ Using: $VENV_PYTHON"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install packages
echo ""
echo "Installing required packages..."
echo "  - chromadb"
echo "  - langchain"
echo "  - langchain-community"
echo "  - langchain-openai"
echo "  - langchain-text-splitters"
echo "  - python-dotenv"
echo ""

pip install chromadb langchain langchain-community langchain-openai \
            langchain-text-splitters python-dotenv beautifulsoup4 requests

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All packages installed successfully!"
else
    echo ""
    echo "❌ Package installation failed"
    exit 1
fi

# Verify ChromaDB installation
echo ""
echo "Verifying ChromaDB installation..."
python -c "import chromadb; print('✓ ChromaDB version:', chromadb.__version__)"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================================"
    echo " ✅ Setup Complete!"
    echo "========================================================================"
    echo ""
    echo "Your virtual environment is ready!"
    echo ""
    echo "To use it:"
    echo "  1. Activate: source venv_py312/bin/activate"
    echo "  2. Load embeddings to ChromaDB: python load_to_chromadb.py"
    echo "  3. When done: deactivate"
    echo ""
    echo "Current status: Environment is ACTIVATED ✅"
    echo "You can now run: python load_to_chromadb.py"
    echo ""
else
    echo ""
    echo "❌ ChromaDB verification failed"
fi
