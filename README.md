<div align="center">

# 🛠️ git-undo

**Fix Git mistakes using natural language—because we've all been there!**

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Git](https://img.shields.io/badge/Git-Ready-orange.svg)](https://git-scm.com/)

</div>

---

## ✨ Features

- 🎯 **Natural Language Interface**: Just describe your mistake in plain English
- 🔍 **Context-Aware**: Automatically analyzes your repo's current state (branch, commits, status, stashes)
- 📝 **Explanations Included**: Every command comes with a clear explanation
- ⚠️ **Destructive Command Warnings**: Prominently flags commands like `git reset --hard` or `git push --force`
- 👀 **Dry-Run Mode**: Preview commands before executing anything
- ✅ **Confirmation Required**: No commands run without your explicit approval
- 🎨 **Beautiful UI**: Powered by `rich` for a clean, colorful interface
- 🌐 **Multi-Provider Support**: Use your favorite AI!

---

## 🤖 Supported Providers & Models

| Provider | Models | Notes |
|----------|--------|-------|
| **OpenAI** | gpt-4o, gpt-4o-mini, etc. | Great all-around choice |
| **OpenRouter** | 100+ models (Anthropic, OpenAI, DeepSeek, Gemini, etc.) | One key for all models |
| **Anthropic** | claude-sonnet-4-5, claude-opus-4-5, claude-haiku-3-5, etc. | Top-tier reasoning |
| **Gemini** | gemini-2.0-flash, gemini-1.5-pro, etc. | Free tier available |
| **DeepSeek** | deepseek-chat, deepseek-reasoner | Fast & affordable |
| **Ollama** | llama3.2, deepseek-r1, qwen2.5-coder, etc. | 100% local, no API key needed |

---

## 🚀 Quick Start

### Prerequisites
1. **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2. **Git**: [Download Git](https://git-scm.com/downloads)
3. An API key from your preferred provider

### Installation
#### Option 1: Install from GitHub (Recommended)
```bash
pip install git+https://github.com/sahik67/git-undo.git
```

#### Option 2: Install Locally (Development)
```bash
# Clone the repo
git clone https://github.com/sahik67/git-undo.git
cd git-undo

# Create virtual environment (Windows)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Create virtual environment (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e .
```

### Configuration
1. Copy the example `.env` file:
   ```bash
   # Windows
   Copy-Item .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. Open `.env` and add your keys (here's an OpenRouter example):
   ```env
   GIT_UNDO_PROVIDER=openrouter
   GIT_UNDO_MODEL=nex-agi/nex-n2-pro:free
   OPENROUTER_API_KEY=sk-or-v1-...your-key...
   ```

### Usage
```bash
# Preview first (ALWAYS recommended!)
git-undo "I accidentally committed to main" --dry-run

# Fix for real
git-undo "I accidentally committed to main"
```

---

## 📖 A-Z Detailed Tutorial

Check out the [full A-Z tutorial](#a-z-detailed-tutorial-1) in the README below!

---

## 📸 Demo

![git-undo in action](./demo.gif)

### How to Make Your Own Demo GIF
1. Record with OBS Studio, Xbox Game Bar (Windows), or QuickTime Player (macOS)
2. Convert to GIF using [ezgif.com](https://ezgif.com/) or ffmpeg:
   ```bash
   ffmpeg -i your-video.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" demo.gif
   ```

---

## ⚙️ Configuration

See the example `.env.example` file for all options!

---

## 🔒 Security Notes

- 🔑 Your API keys are stored locally and **never** shared
- ⚠️ Destructive commands always trigger a large warning
- 👀 Always use `--dry-run` first to preview changes
- ✅ No commands execute without your explicit confirmation

---

## 📄 License

MIT License — See [LICENSE](./LICENSE) file for details!

---

<div align="center">
Made with ❤️ by sahik
</div>

---

## A-Z Detailed Tutorial

### Step 1: Configure API Keys
1. Copy the example environment file:
   - **Windows**:
     ```powershell
     Copy-Item .env.example .env
     ```
   - **macOS/Linux**:
     ```bash
     cp .env.example .env
     ```
2. Open `.env` in a text editor and add your API keys:
   - For OpenRouter (recommended - one key for 100+ models):
     ```env
     GIT_UNDO_PROVIDER=openrouter
     GIT_UNDO_MODEL=nex-agi/nex-n2-pro:free
     OPENROUTER_API_KEY=sk-or-v1-...your-key-here...
     ```
   - For OpenAI:
     ```env
     GIT_UNDO_PROVIDER=openai
     OPENAI_API_KEY=sk-...your-key-here...
     ```

### Step 2: Prepare a Test Git Repository
Let's create a simple test repository to practice with:
1. Create a new folder for your test repo:
   ```bash
   mkdir git-undo-test
   cd git-undo-test
   ```
2. Initialize Git and make a test commit:
   ```bash
   git init
   echo "Hello world!" > test.txt
   git add test.txt
   git commit -m "Initial commit"
   ```
3. Make a "mistake" to fix! Let's add a wrong file and commit it:
   ```bash
   echo "Oops, wrong file!" > wrong-file.txt
   git add wrong-file.txt
   git commit -m "Add wrong file by mistake"
   ```

### Step 3: Run git-undo!
Now let's fix our mistake using git-undo:
1. First, use `--dry-run` to preview the commands without executing them:
   ```bash
   git-undo "I accidentally committed wrong-file.txt" --dry-run
   ```
   You should see a beautiful UI with suggested commands!
2. If you're happy with the commands, run git-undo without `--dry-run` to execute them:
   ```bash
   git-undo "I accidentally committed wrong-file.txt"
   ```
3. Confirm the action when prompted, and git-undo will fix your mistake!

## Usage Examples

```bash
# Preview commands without executing them
git-undo I deleted a branch by mistake --dry-run

# Fix a wrong commit
git-undo I committed the wrong files

# Recover stashed changes
git-undo I lost my stash

# Fix a merge conflict
git-undo "I messed up the merge conflict resolution"

# Undo a git push --force
git-undo "I accidentally force pushed to main" --dry-run
```
