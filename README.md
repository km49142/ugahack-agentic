# AI Internship Application Bot (testBranch)

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
Start the bot and choose to enable the AI Agent:
```bash
python apply.py
```

---

## ✨ Key Features

- 🤖 **AI Agent**: Uses LLMs (Anthropic Claude or local TensorFlow) to answer open-ended questions based on your profile.
- 🔐 **Smart Automation**: Detects login/signup pages, handles account creation, and fills complex forms.
- 📄 **Document Upload**: Automatically attaches your resume and transcripts.
- 📊 **Tracking & Review**: Logs all applications to `data/applications.csv` and saves screenshots for review.
- 🛠️ **Developer Tools**: Includes smoke tests and agent-specific testing suites.

## 📂 Project Structure

```
ugahack-agentic/
├── src/
│   ├── agent.py                # AI Agent orchestrator
│   ├── llm_client.py           # Anthropic & TensorFlow clients
│   ├── form_filler.py          # Field detection (now with AI fallback)
│   └── ... (core logic)
├── scripts/                    # Maintenance & smoke test scripts
├── tests/                      # Unit and integration tests
├── setup_profile.py            # CLI: Configure your profile
└── apply.py                    # CLI: Apply to jobs (with AI opt-in)
```

## 💡 AI Configuration

- **Anthropic**: Requires `ANTHROPIC_API_KEY` environment variable.
- **TensorFlow**: Uses a local `universal-sentence-encoder-qa` model (no API key required, but requires `tensorflow` and `tensorflow_hub` packages).

## ⚠️ Important Notes

- **Preview Mode**: Enabled by default. Review screenshots in `data/screenshots/` before submitting.
- **Privacy**: All profile data is stored locally in `data/user_profile.json`.

---
*Developed for UgaHacks. AI Agent experimental features.*