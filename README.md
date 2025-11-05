# 🤖 AI-Powered Test Case Generator

**Automatically generate comprehensive test cases from user stories using AI.**

Perfect for QA engineers, developers, and product managers who want to ensure thorough testing coverage without spending hours writing test cases manually.

---

## 📋 Table of Contents

- [What Does This Tool Do?](#what-does-this-tool-do)
- [Why Is This Useful?](#why-is-this-useful)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Usage Guide](#usage-guide)
- [Understanding Test Cases](#understanding-test-cases)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Cost Information](#cost-information)

---

## 🎯 What Does This Tool Do?

This tool takes a **user story** (a description of what a user wants to do) and automatically generates multiple comprehensive **test cases** using AI.

**Input Example:**
```
As a user, I want to login with email and password so that I can access my dashboard
```

**Output:** 5-10 detailed test cases covering:
- ✅ Happy path (everything works correctly)
- ❌ Error scenarios (invalid inputs, wrong passwords, etc.)
- 🔒 Security tests (SQL injection, XSS, etc.)
- 📏 Edge cases (empty fields, special characters, etc.)

---

## 💡 Why Is This Useful?

### For QA Engineers:
- **Save Time**: Generate test cases in seconds instead of hours
- **Comprehensive Coverage**: AI suggests scenarios you might have missed
- **Consistent Format**: All test cases follow the same structure

### For Developers:
- **Better Testing**: Know exactly what to test before deploying
- **Documentation**: Auto-generate test documentation
- **Quality Assurance**: Catch bugs early in development

### For Product Managers:
- **Acceptance Criteria**: Generate detailed acceptance criteria from user stories
- **Risk Assessment**: Identify potential issues before development
- **Communication**: Clear test cases help align team understanding

---

## 📦 Prerequisites

Before you begin, you need:

1. **Python 3.8 or higher**
   - Check: Open terminal and run `python3 --version`
   - Install: Download from [python.org](https://www.python.org/downloads/)

2. **OpenAI API Key**
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Create API key at [API Keys page](https://platform.openai.com/api-keys)
   - Note: This service costs money (usually pennies per request)

3. **Basic Terminal Knowledge**
   - How to navigate directories (`cd`)
   - How to run commands

---

## 🚀 Installation

### Step 1: Clone or Download This Repository

```bash
# If you have git:
git clone https://github.com/yourusername/ai-test-case-generator.git
cd ai-test-case-generator

# Or download the ZIP file and extract it
```

### Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps this project's dependencies separate from other Python projects.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai`: Connect to OpenAI's API
- `python-dotenv`: Manage configuration securely
- `click`: Create command-line interface
- `colorama`: Add colors to terminal output

### Step 4: Configure Your API Key

**Option A: Interactive Setup (Easiest)**
```bash
python cli.py setup
```

**Option B: Manual Setup**
```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your API key
# OPENAI_API_KEY=your-actual-api-key-here
```

**🔒 Security Note:** Never commit your `.env` file to Git! It's already in `.gitignore`.

---

## ⚡ Quick Start

### Generate Your First Test Cases

```bash
python cli.py generate "As a user, I want to login with email and password"
```

This will:
1. Connect to OpenAI's API
2. Generate 5 test cases
3. Display them in your terminal with colors

### Save to a File

```bash
# Save as Markdown (human-readable)
python cli.py generate "Your user story" --output tests.md

# Save as JSON (machine-readable)
python cli.py generate "Your user story" --output tests.json
```

### Generate More Test Cases

```bash
# Generate 10 test cases instead of 5
python cli.py generate "Your user story" --count 10
```

### Focus on Specific Areas

```bash
# Focus on security testing
python cli.py generate "Your user story" --focus security

# Multiple focus areas
python cli.py generate "Your user story" --focus security --focus performance
```

---

## 🔍 How It Works

Here's what happens when you generate test cases:

```
1. You provide a user story
   ↓
2. Tool creates a detailed prompt for AI
   ↓
3. Sends request to OpenAI's API
   ↓
4. AI generates structured test cases
   ↓
5. Tool parses and formats the response
   ↓
6. Displays/saves test cases
```

**Under the Hood:**
- Uses GPT-3.5-turbo (fast and cost-effective) by default
- Can upgrade to GPT-4 for more complex scenarios
- Enforces JSON output format for consistency
- Handles errors and retries automatically

---

## 📖 Usage Guide

### Basic Command Structure

```bash
python cli.py [COMMAND] [OPTIONS] [ARGUMENTS]
```

### Available Commands

#### 1. `generate` - Generate test cases from a user story

```bash
python cli.py generate "Your user story here" [OPTIONS]
```

**Options:**
- `--count, -c`: Number of test cases to generate (default: 5)
- `--model, -m`: AI model to use (default: gpt-3.5-turbo)
- `--output, -o`: Save to file (.json or .md)
- `--focus, -f`: Focus areas (can use multiple times)

**Examples:**
```bash
# Basic
python cli.py generate "As a user, I want to reset my password"

# Advanced
python cli.py generate "User story" --count 10 --output tests.md --focus security --focus performance
```

#### 2. `batch` - Process multiple user stories from a file

```bash
python cli.py batch stories.txt [OPTIONS]
```

**File Format:** One user story per line

```text
As a user, I want to login with email and password
As a user, I want to reset my forgotten password
As a user, I want to update my profile information
```

**Options:**
- `--count, -c`: Test cases per story (default: 5)
- `--output-dir, -o`: Output directory (default: output/)

**Example:**
```bash
python cli.py batch my_stories.txt --count 8 --output-dir test_results
```

#### 3. `setup` - Interactive configuration

```bash
python cli.py setup
```

Walks you through setting up your API key.

#### 4. `examples` - Show examples

```bash
python cli.py examples
```

Displays example user stories and commands.

---

## 📚 Understanding Test Cases

### What Is a Test Case?

A test case is a set of instructions to verify that a feature works correctly.

**Components of a Test Case:**

1. **Title**: Brief description of what's being tested
2. **Description**: Detailed explanation of the test purpose
3. **Preconditions**: What must be set up before testing
4. **Steps**: Numbered instructions to follow
5. **Expected Result**: What should happen if feature works
6. **Test Type**: Category of test (see below)
7. **Priority**: How important this test is

### Test Types Explained

#### Unit Test
- **What**: Tests a single function or component
- **Example**: "Test that email validation function rejects invalid emails"
- **When**: During development of individual features

#### Integration Test
- **What**: Tests how multiple components work together
- **Example**: "Test that login form connects to authentication service"
- **When**: After unit tests pass, before full system testing

#### E2E (End-to-End) Test
- **What**: Tests complete user workflows
- **Example**: "Test entire login flow from entering credentials to viewing dashboard"
- **When**: Before releasing to production

### Test Scenarios

#### Positive Tests (Happy Path)
- Everything works as expected
- Valid inputs, normal conditions
- Example: "User enters correct email and password, successfully logs in"

#### Negative Tests
- Things that shouldn't work
- Invalid inputs, error conditions
- Example: "User enters wrong password, login fails with error message"

#### Edge Cases
- Boundary conditions and unusual scenarios
- Example: "User enters maximum allowed character length in password field"

#### Security Tests
- Potential vulnerabilities
- Example: "System blocks SQL injection attempt in login form"

---

## 💡 Examples

### Example 1: Login Feature

**User Story:**
```
As a user, I want to login with email and password so that I can access my dashboard
```

**Command:**
```bash
python cli.py generate "As a user, I want to login with email and password so that I can access my dashboard" --count 6 --focus security
```

**Generated Test Cases Include:**
- ✅ Successful login with valid credentials
- ❌ Login failure with incorrect password
- ❌ Login failure with non-existent email
- 🔒 SQL injection attempt in email field
- 📏 Empty email or password fields
- 🔐 Account lockout after multiple failed attempts

### Example 2: Shopping Cart

**User Story:**
```
As a customer, I want to add items to my cart so that I can purchase multiple products at once
```

**Command:**
```bash
python cli.py generate "As a customer, I want to add items to my cart so that I can purchase multiple products at once" --output cart_tests.md
```

### Example 3: File Upload

**User Story:**
```
As a user, I want to upload profile pictures up to 5MB so that I can personalize my account
```

**Command:**
```bash
python cli.py generate "As a user, I want to upload profile pictures up to 5MB so that I can personalize my account" --focus security --focus performance
```

---

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not found"

**Problem:** API key is not configured.

**Solution:**
```bash
# Run setup
python cli.py setup

# Or manually create .env file with:
# OPENAI_API_KEY=your-key-here
```

### Error: "Import 'openai' could not be resolved"

**Problem:** Dependencies not installed.

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Error: "API rate limit exceeded"

**Problem:** Too many requests to OpenAI in short time.

**Solution:**
- Wait a few seconds between requests
- Check your OpenAI account usage limits
- Consider upgrading your OpenAI plan

### Error: "Invalid API key"

**Problem:** API key is incorrect or expired.

**Solution:**
- Verify key at [OpenAI API Keys](https://platform.openai.com/api-keys)
- Generate new key if needed
- Update .env file with correct key

### Test Cases Seem Generic

**Problem:** Not enough context in user story.

**Solution:** Provide more detailed user stories:

❌ Bad: "User wants to login"
✅ Good: "As a registered user, I want to login with my email and password, with optional 'Remember Me' checkbox, so that I can access my personalized dashboard showing recent orders"

---

## 💰 Cost Information

This tool uses OpenAI's API, which charges per request.

**Typical Costs (as of 2024):**
- GPT-3.5-turbo: ~$0.001-0.002 per test case generation
- GPT-4: ~$0.01-0.03 per test case generation

**Example:**
- Generating 100 test cases with GPT-3.5: ~$0.10-0.20
- Generating 100 test cases with GPT-4: ~$1-3

**Tips to Reduce Costs:**
1. Use GPT-3.5-turbo (default) for most cases
2. Generate reasonable number of test cases (5-10)
3. Review and refine user stories before generating
4. Use batch processing for multiple stories

**Check your usage:**
- [OpenAI Usage Dashboard](https://platform.openai.com/usage)

---

## 🤝 Best Practices

### Writing Good User Stories

Follow the format:
```
As a [type of user], I want to [action], so that [benefit/reason]
```

**Good Examples:**
- "As a customer, I want to track my order status so that I know when it will arrive"
- "As an admin, I want to export user data to CSV so that I can analyze it in Excel"

**Bad Examples:**
- "Login feature" (too vague)
- "Make the app better" (no specific action)

### Using Generated Test Cases

1. **Review**: Always review AI-generated tests
2. **Customize**: Adapt to your specific requirements
3. **Combine**: Use alongside manual test cases
4. **Iterate**: Refine user stories based on results
5. **Integrate**: Import into test management tools

---

## 📝 Project Structure

```
ai-test-case-generator/
├── cli.py                    # Command-line interface
├── test_case_generator.py    # Main generator logic
├── requirements.txt          # Python dependencies
├── .env.example             # Example configuration
├── .env                     # Your API key (not in git)
├── .gitignore              # Files to exclude from git
├── README.md               # This file
└── examples/               # Example user stories
    └── sample_stories.txt
```

---

## 🎓 Learning Resources

### Testing Concepts
- [Software Testing Fundamentals](https://softwaretestingfundamentals.com/)
- [Test Case Writing Best Practices](https://www.guru99.com/test-case.html)

### User Stories
- [User Story Guide](https://www.atlassian.com/agile/project-management/user-stories)

### DevOps
- [DevOps Roadmap](https://roadmap.sh/devops)

---

## 🆘 Getting Help

1. **Check Examples**: Run `python cli.py examples`
2. **Read Error Messages**: They usually explain the problem
3. **Review This README**: Use the troubleshooting section
4. **Check OpenAI Status**: [status.openai.com](https://status.openai.com)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Credits

Built with:
- [OpenAI API](https://openai.com/) - AI model
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Colorama](https://pypi.org/project/colorama/) - Terminal colors

---

**Happy Testing! 🚀**

*Remember: AI-generated test cases are a starting point. Always review and adapt them to your specific needs.*
