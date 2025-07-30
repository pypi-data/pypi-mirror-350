# 🧠 cmitai

**cmitai** is a modern CLI tool that generates helpful and concise Git commit messages based on staged changes, using LLMs like OpenAI or Google Gemini.

---

## ✨ Features

- 🔍 Analyzes `git diff --cached` to understand your staged changes
- 🤖 Supports OpenAI (GPT-3.5, GPT-4) and Google Gemini (e.g., Gemini 1.5 Flash)
- ⚡ Fast and simple CLI built with [Typer](https://typer.tiangolo.com/)
- ✅ Supports `.commitai.json` configuration per project
- 📦 Modern Python packaging with `pyproject.toml` and `src/` layout

---

## 📦 Installation

### From PyPI (when published):

```bash
pip install cmitai
```

### For local development:

```bash
uv pip install -e .
```

---

## 🚀 Usage

First, stage your changes:

```bash
git add .
```

Then run:

```bash
cmitai generate commit
```

This will analyze the diff of staged files and return a suggested commit message.

---

## 🔐 Configuration

Create a `.commitai.json` file at the **root of your Git project**:

### Example for OpenAI:

```json
{
  "agent_type": "openai",
  "api_key": "sk-..."
}
```

### Example for Google Gemini:

```json
{
  "agent_type": "gemini",
  "api_key": "your-gemini-api-key"
}
```

✅ Recommended Gemini model for free tier: `"models/gemini-1.5-flash"`

---

## 🧪 Example Output

```bash
❯ git add main.py
❯ cmitai generate commit

Suggested commit message:
Improve error handling in main.py for API failures
```

---

## 🛠 Developer workflow

Use the included `Makefile` for common tasks:

```bash
make lint     # Run Ruff linter with auto-fix
make format   # Format code with Ruff
make test     # Run tests with Pytest
make check    # Lint + format
```

---

## 📁 Project structure

```
cmitai/
├── src/
│   └── cmitai/
│       ├── cli/
│       ├── configs/
│       ├── git_ops/
│       ├── llm/
│       ├── main.py
├── pyproject.toml
├── README.md
├── Makefile
├── LICENSE
└── .commitai.json  # not versioned
```

---

## 📄 License

MIT © [Your Name]
