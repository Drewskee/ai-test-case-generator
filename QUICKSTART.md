# Quick Start Guide

Get up and running in 5 minutes!

## 1️⃣ Install (First Time Only)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## 2️⃣ Configure API Key (First Time Only)

```bash
# Interactive setup
python cli.py setup

# Enter your OpenAI API key when prompted
# Get key from: https://platform.openai.com/api-keys
```

## 3️⃣ Generate Test Cases

```bash
# Basic usage
python cli.py generate "As a user, I want to login with email and password"

# Save to file
python cli.py generate "Your user story" --output tests.md

# Generate more tests
python cli.py generate "Your user story" --count 10

# Focus on security
python cli.py generate "Your user story" --focus security
```

## 🎯 Common Commands

```bash
# See examples
python cli.py examples

# Process multiple stories
python cli.py batch examples/sample_stories.txt

# Get help
python cli.py --help
python cli.py generate --help
```

## 🔧 Daily Usage

```bash
# 1. Activate virtual environment (do this every time you open terminal)
source venv/bin/activate

# 2. Generate test cases
python cli.py generate "Your user story here"

# 3. When done, deactivate (optional)
deactivate
```

## ❓ Troubleshooting

**"OPENAI_API_KEY not found"**
→ Run `python cli.py setup` and enter your API key

**"command not found: python"**
→ Try `python3` instead of `python`

**"Import 'openai' could not be resolved"**
→ Make sure you activated venv and ran `pip install -r requirements.txt`

---

📖 **For detailed documentation, see [README.md](README.md)**
