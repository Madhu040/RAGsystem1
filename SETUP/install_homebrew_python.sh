#!/bin/bash

# Step-by-Step Installation Script for Python 3.12 on macOS
# Run this in Terminal

echo "========================================================================"
echo " Installing Python 3.12 for ChromaDB"
echo "========================================================================"
echo ""

# Check if Homebrew is installed
if command -v brew &> /dev/null; then
    echo "✅ Homebrew is already installed"
    echo ""
else
    echo "📦 Homebrew is not installed. Installing now..."
    echo ""
    echo "This will:"
    echo "  1. Install Homebrew (package manager for macOS)"
    echo "  2. May ask for your password"
    echo "  3. Take 5-10 minutes"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to cancel..."
    
    # Install Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Check if installation was successful
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Homebrew installed successfully!"
        
        # Add Homebrew to PATH for current session
        # Check if on Apple Silicon or Intel
        if [[ $(uname -m) == "arm64" ]]; then
            echo "export PATH=/opt/homebrew/bin:\$PATH" >> ~/.zshrc
            export PATH=/opt/homebrew/bin:$PATH
            echo "✓ Added Homebrew to PATH (Apple Silicon)"
        else
            echo "export PATH=/usr/local/bin:\$PATH" >> ~/.zshrc
            export PATH=/usr/local/bin:$PATH
            echo "✓ Added Homebrew to PATH (Intel)"
        fi
        
        source ~/.zshrc
        echo ""
    else
        echo "❌ Homebrew installation failed"
        echo "Please try manually at: https://brew.sh"
        exit 1
    fi
fi

# Verify brew is now available
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew not found in PATH"
    echo ""
    echo "Please run these commands:"
    if [[ $(uname -m) == "arm64" ]]; then
        echo "  echo 'export PATH=/opt/homebrew/bin:\$PATH' >> ~/.zshrc"
    else
        echo "  echo 'export PATH=/usr/local/bin:\$PATH' >> ~/.zshrc"
    fi
    echo "  source ~/.zshrc"
    echo ""
    echo "Then run this script again"
    exit 1
fi

# Now install Python 3.12
echo "========================================================================"
echo " Installing Python 3.12"
echo "========================================================================"
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

# Find Python 3.12
if command -v python3.12 &> /dev/null; then
    PYTHON_VERSION=$(python3.12 --version)
    echo "✅ $PYTHON_VERSION is available"
else
    echo "⚠️  python3.12 command not found, trying brew path..."
    if [[ $(uname -m) == "arm64" ]]; then
        PYTHON312="/opt/homebrew/bin/python3.12"
    else
        PYTHON312="/usr/local/bin/python3.12"
    fi
    
    if [ -f "$PYTHON312" ]; then
        PYTHON_VERSION=$($PYTHON312 --version)
        echo "✅ $PYTHON_VERSION found at $PYTHON312"
    fi
fi

echo ""
echo "========================================================================"
echo " ✅ Installation Complete!"
echo "========================================================================"
echo ""
echo "Next steps:"
echo "  1. Close and reopen Terminal (or run: source ~/.zshrc)"
echo "  2. Navigate to your project:"
echo "     cd /Users/madhu/Downloads/Cursor_all/AI-ENG-Boot-CAMP/WEEK2-POC"
echo "  3. Run setup script:"
echo "     ./install_chromadb_env.sh"
echo ""
