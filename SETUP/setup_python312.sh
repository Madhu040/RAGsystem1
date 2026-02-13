#!/bin/bash

# Python 3.12 Installation and Setup Guide for ChromaDB
# This script helps you install Python 3.12 and set up the environment

echo "========================================================================"
echo " Python 3.12 Installation Guide for ChromaDB Compatibility"
echo "========================================================================"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew first..."
    echo ""
    echo "Run this command:"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo ""
    echo "After Homebrew is installed, run this script again."
    exit 1
fi

echo "✓ Homebrew is installed"
echo ""

# Install Python 3.12
echo "========================================================================"
echo "Step 1: Installing Python 3.12"
echo "========================================================================"
echo ""
echo "Running: brew install python@3.12"
echo ""

brew install python@3.12

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Python 3.12 installed successfully!"
else
    echo ""
    echo "❌ Python 3.12 installation failed"
    exit 1
fi

# Find Python 3.12 path
PYTHON312_PATH=$(brew --prefix python@3.12)/bin/python3.12

echo ""
echo "✓ Python 3.12 location: $PYTHON312_PATH"
echo ""

# Create virtual environment
echo "========================================================================"
echo "Step 2: Creating Virtual Environment with Python 3.12"
echo "========================================================================"
echo ""

cd "$(dirname "$0")"
echo "Working directory: $(pwd)"
echo ""

if [ -d "venv_py312" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv_py312
fi

echo "Creating virtual environment: venv_py312"
$PYTHON312_PATH -m venv venv_py312

if [ $? -eq 0 ]; then
    echo "✅ Virtual environment created!"
else
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate and install packages
echo ""
echo "========================================================================"
echo "Step 3: Installing Required Packages"
echo "========================================================================"
echo ""

source venv_py312/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Installing packages..."
pip install -q chromadb langchain langchain-community langchain-openai langchain-text-splitters python-dotenv beautifulsoup4 requests

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully!"
else
    echo "❌ Package installation failed"
    exit 1
fi

# Verify installation
echo ""
echo "========================================================================"
echo "Step 4: Verifying Installation"
echo "========================================================================"
echo ""

python --version
echo ""
python -c "import chromadb; print('✓ ChromaDB version:', chromadb.__version__)"
python -c "import langchain; print('✓ LangChain installed')"
python -c "import langchain_openai; print('✓ LangChain OpenAI installed')"

echo ""
echo "========================================================================"
echo "✅ SETUP COMPLETE!"
echo "========================================================================"
echo ""
echo "📝 How to use:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv_py312/bin/activate"
echo ""
echo "2. Run your ChromaDB scripts:"
echo "   python load_to_chromadb.py"
echo ""
echo "3. When done, deactivate:"
echo "   deactivate"
echo ""
echo "========================================================================"
