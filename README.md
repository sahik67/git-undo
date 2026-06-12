# git-undo

A CLI tool to fix Git mistakes using natural language powered by multiple AI providers.

## Supported Providers & Models
- **OpenAI**: gpt-4o, gpt-4o-mini, etc.
- **OpenRouter**: Access to 100+ models (Anthropic, OpenAI, DeepSeek, Gemini, etc.) with one API key
- **Anthropic**: claude-sonnet-4-5, claude-opus-4-5, claude-haiku-3-5, etc.
- **Gemini**: gemini-2.0-flash, gemini-1.5-pro, etc.
- **DeepSeek**: deepseek-chat, deepseek-reasoner
- **Ollama**: Local models like llama3.2, deepseek-r1, qwen2.5-coder, etc.

## Features

- Describe your Git mistake in plain English
- Automatically analyzes your repository's current state
- Generates and displays safe, context-aware Git commands with explanations
- Flags destructive commands with prominent warnings
- Requires explicit confirmation before executing commands
- Real-time output streaming for executed commands

## Prerequisites
Before installing git-undo, make sure you have:
1. **Python 3.10 or higher**: Download from https://www.python.org/downloads/
2. **Git**: Download from https://git-scm.com/downloads
3. An API key from your preferred AI provider (e.g., OpenRouter, OpenAI, Anthropic, etc.)

## Installation

### Option 1: Install from PyPI (when published)
```bash
pip install git-undo
```

### Option 2: Install from GitHub
```bash
pip install git+https://github.com/sahik67/git-undo.git
```

### Option 3: Install from Local Source (Development)
1. Clone or download the repo:
   ```bash
   git clone https://github.com/sahik67/git-undo.git
   cd git-undo
   ```
2. Create a virtual environment (optional but recommended):
   - **Windows**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

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
   You should see:
   ```
   Suggested Commands:

   ╭─────────────────────────── ⚠️  Command 1 (DESTRUCTIVE) ───────────────────────────╮
   │ git reset --hard HEAD~1                                                          │
   ╰───────────────────────────────────────────────────────────────────────────────────╯
   Removes the last commit which added wrong-file.txt.

   ╭────────────────────────── Destructive Commands Detected ──────────────────────────╮
   │ ⚠️  WARNING: One or more commands are destructive and may result in data loss!    │
   ╰───────────────────────────────────────────────────────────────────────────────────╯

   Dry run complete - no commands executed
   ```
2. If you're happy with the commands, run git-undo without `--dry-run` to execute them:
   ```bash
   git-undo "I accidentally committed wrong-file.txt"
   ```
3. Confirm the action when prompted, and git-undo will fix your mistake!

## Configuration
Create a `.env` file in your project or set environment variables:

### Example .env File
```env
# Provider selection (options: openai, openrouter, anthropic, gemini, deepseek, ollama)
GIT_UNDO_PROVIDER=openrouter
GIT_UNDO_MODEL=~anthropic/claude-fable-latest

# OpenAI API Key
OPENAI_API_KEY=sk-...

# OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-...

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-...

# Google (Gemini) API Key
GOOGLE_API_KEY=...

# DeepSeek API Key
DEEPSEEK_API_KEY=sk-...

# Ollama Base URL (default: http://localhost:11434/v1)
OLLAMA_BASE_URL=http://localhost:11434/v1
```

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

## Demo

![git-undo in action](./demo.gif)

### How to Create Your Own Demo GIF
1. Install a screen recorder like:
   - Windows: **OBS Studio** (free) or **Xbox Game Bar** (built-in)
   - macOS: **OBS Studio** or **QuickTime Player** (built-in)
   - Linux: **OBS Studio** or **Peek**
2. Record a video of you using git-undo (follow the A-Z tutorial above)
3. Convert the video to a GIF using an online tool like https://ezgif.com/ or a local tool like `ffmpeg`:
   ```bash
   ffmpeg -i your-recording.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" demo.gif
   ```
4. Replace `demo.gif` in the repo with your new GIF!

## Security Notes

- git-undo flags and warns you about destructive commands (like `git push --force`, `git reset --hard`, etc.)
- Always use `--dry-run` first to preview commands
- No commands are executed without your explicit confirmation
- Your API keys are stored locally and never shared

## License

MIT
