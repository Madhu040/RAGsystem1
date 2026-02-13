# 🔧 Fix: "brew: command not found"

## The Problem
You don't have **Homebrew** installed yet. Homebrew is a package manager for macOS that you need to install Python 3.12.

---

## 📋 Step-by-Step Solution

### Step 1: Install Homebrew

Open **Terminal** and paste this command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**What this does:**
- Installs Homebrew (macOS package manager)
- Will ask for your password
- Takes about 5-10 minutes
- Follow any instructions it shows

### Step 2: Add Homebrew to Your PATH

After Homebrew installs, it will show you commands to run. They look like this:

**For Apple Silicon (M1/M2/M3 Mac):**
```bash
echo 'export PATH=/opt/homebrew/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```

**For Intel Mac:**
```bash
echo 'export PATH=/usr/local/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Verify Homebrew Works

```bash
brew --version
```

You should see something like: `Homebrew 4.x.x`

---

## 🚀 Once Homebrew is Installed

### Then Run These Commands:

```bash
# 1. Install Python 3.12
brew install python@3.12

# 2. Go to your project folder
cd /Users/madhu/Downloads/Cursor_all/AI-ENG-Boot-CAMP/WEEK2-POC

# 3. Create virtual environment
python3.12 -m venv venv_py312

# 4. Activate it
source venv_py312/bin/activate

# 5. Install packages
pip install --upgrade pip
pip install chromadb langchain langchain-community langchain-openai langchain-text-splitters python-dotenv

# 6. Load your embeddings to ChromaDB
python load_to_chromadb.py
```

---

## 🎯 Or Use the Automated Scripts

I created scripts to automate this for you:

### Option A: Install Everything Step by Step

```bash
cd /Users/madhu/Downloads/Cursor_all/AI-ENG-Boot-CAMP/WEEK2-POC

# First, install Homebrew and Python 3.12
./install_homebrew_python.sh

# After that completes, install ChromaDB environment
./install_chromadb_env.sh

# Load embeddings
python load_to_chromadb.py
```

### Option B: Manual Commands (Safer)

If scripts don't work, use the manual commands in Step 1-3 above.

---

## ❓ Common Issues

### "Permission denied"
If you get permission errors:
```bash
sudo chown -R $(whoami) /opt/homebrew  # Apple Silicon
# or
sudo chown -R $(whoami) /usr/local     # Intel
```

### "xcrun: error: invalid active developer path"
You need to install Xcode Command Line Tools first:
```bash
xcode-select --install
```

### "brew still not found after install"
Close Terminal completely and reopen it, then try again.

---

## ⏱️ How Long Does This Take?

- **Installing Homebrew**: 5-10 minutes
- **Installing Python 3.12**: 2-3 minutes
- **Setting up environment**: 1-2 minutes
- **Loading embeddings**: Less than 1 minute

**Total: About 10-15 minutes**

---

## 💡 Alternative: Download Python 3.12 Directly

If Homebrew doesn't work, you can download Python 3.12 directly:

1. Go to: https://www.python.org/downloads/
2. Download **Python 3.12.x for macOS**
3. Run the installer
4. Then use `python3.12` commands from Step 3 onwards

---

## 🆘 Still Having Issues?

Check your Terminal output and look for:
- Error messages
- Commands it tells you to run
- Warnings about PATH

Run this to diagnose:
```bash
which python3
ls -la /opt/homebrew/bin/  # Apple Silicon
ls -la /usr/local/bin/      # Intel
echo $PATH
```

---

## 📞 Quick Reference Card

```bash
# Check if Homebrew installed
brew --version

# Check if Python 3.12 installed  
python3.12 --version

# Check current Python
python3 --version

# Activate virtual environment
source venv_py312/bin/activate

# Check if in virtual environment
which python
```

---

**Start with Step 1 above and let me know if you hit any errors!**
