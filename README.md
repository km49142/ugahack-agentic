# AI Internship Application Bot

An intelligent automation tool for internship applications, now featuring **AI-powered field answering**.

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Setup Your Profile
Run the interactive setup to store your information locally:
```bash
python setup_profile.py
```

### 3. Apply with AI
Start the bot and follow the prompts. You can choose to enable the AI Agent for complex questions:
```bash
python apply.py
```

---

## ✨ Features

- 🤖 **AI Agent**: Uses LLMs (Anthropic Claude or local TensorFlow) to answer open-ended or unknown questions based on your profile.
- 🔐 **Account Creation**: Automatically detects login/signup pages and can generate/save credentials.
- 📄 **Smart Form Filling**: Intelligently detects and fills common fields using pattern recognition.
- 📂 **Document Handling**: Automatically uploads resumes and transcripts from your profile.
- 📊 **Tracking**: Logs every application to `data/applications.csv` with status updates.
- 📸 **Preview Mode**: Runs by default without submitting, saving screenshots of filled forms for review.

## 📂 Project Structure

```
ugahack-agentic/
├── src/
│   ├── agent.py                # AI Agent orchestrator
│   ├── llm_client.py           # Anthropic & TensorFlow clients
│   ├── form_filler.py          # Field detection & filling logic
│   ├── application_bot.py       # Main orchestrator
│   └── ... (core logic)
├── scripts/                    # Maintenance & smoke test scripts
├── tests/                      # Unit and integration tests
├── data/                       # Created on first run (Profile & Logs)
├── setup_profile.py            # CLI: Configure your profile
├── apply.py                    # CLI: Start applying
└── requirements.txt            # Dependencies
```

## 💡 AI Configuration

- **Local AI (TensorFlow)**: Uses a local model to answer questions privately on your machine. No API keys are required.
- **Dependencies**: Requires `tensorflow` and `tensorflow_hub` packages. The model will download automatically (~500MB) on the first run.

## ⚠️ Important Notes

- **Preview Mode**: Always review screenshots in `data/screenshots/` before enabling `submit=True`.
- **Security**: Your data is stored locally in `data/user_profile.json`. Never commit the `data/` folder.
- **Limitations**: Cannot solve CAPTCHAs or answer complex multi-page essays (yet).

---
*Developed for UgaHacks. Use responsibly.*