# AI Internship Application Bot

An intelligent automation tool that helps you apply to internships faster using web automation.

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

### 3. Apply to Internships
Run the bot and follow the prompts:
```bash
python apply.py
```

---

## ✨ Features

- 🤖 **Automated Form Filling**: Intelligently detects and fills form fields using pattern recognition.
- 🔐 **Account Creation**: Automatically detects login/signup pages and can generate/save credentials.
- 📄 **Document Handling**: Automatically uploads resumes and transcripts from your profile.
- 📊 **Application Tracking**: Logs every application to `data/applications.csv` with status updates.
- 📸 **Preview Mode**: Runs by default without submitting, saving screenshots of filled forms for your review.
- 🔄 **Interactive Questions**: Asks you for answers to complex questions (e.g., "Do you need sponsorship?") and remembers them.

## 📂 Project Structure

```
ugahack-agentic/
├── src/
│   ├── profile_manager.py      # Manages user profile (JSON)
│   ├── browser_automation.py    # Playwright wrapper
│   ├── form_filler.py          # Field detection & filling logic
│   ├── account_creator.py      # Login/Signup automation
│   ├── application_tracker.py   # CSV tracking logic
│   └── application_bot.py       # Main orchestrator
├── data/                       # Created on first run (Profile & Logs)
├── setup_profile.py            # CLI: Configure your info
├── apply.py                    # CLI: Start applying
└── requirements.txt            # Dependencies
```

## 💡 Important Notes

- **Preview Mode**: The bot runs in preview mode by default. Always review screenshots in `data/screenshots/` before enabling `submit=True`.
- **Security**: Your data (including generated passwords) is stored locally in `data/user_profile.json`. Never commit the `data/` folder to version control.
- **Limitations**: Cannot solve CAPTCHAs or answer complex open-ended essays (yet).

## 🛠️ Requirements

- Python 3.8+
- Playwright (Chromium)
- Pandas (for tracking)

---
*Developed for UgaHacks. Use responsibly.*