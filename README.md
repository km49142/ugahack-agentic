# AI Internship Application Bot

An intelligent automation tool that helps you apply to internships faster using AI and web automation.

## Features

- 🤖 **Automated Form Filling**: Intelligently detects and fills form fields
- 📄 **Resume Parsing**: Extracts information from PDF and DOCX resumes
- 🎯 **Smart Field Detection**: Recognizes common fields (name, email, education, etc.)
- 📊 **Application Tracking**: Tracks all applications with pandas DataFrames
- 🖼️ **Screenshots**: Captures screenshots at each step for review
- 🔄 **Batch Processing**: Apply to multiple jobs in sequence
- ⚡ **Fast & Reliable**: Built with Playwright for modern web applications

## Project Structure

```
ktphacks/
├── src/
│   ├── profile_manager.py      # Manages user profile data
│   ├── resume_parser.py         # Parses resumes (PDF/DOCX)
│   ├── browser_automation.py    # Core Playwright automation
│   ├── form_filler.py          # Detects and fills forms
│   ├── application_tracker.py   # Tracks applications
│   └── application_bot.py       # Main orchestrator
├── data/
│   ├── user_profile.json       # Your profile data
│   ├── applications.csv        # Application history
│   └── screenshots/            # Screenshots from applications
├── example_usage.py            # Usage examples
└── requirements.txt            # Python dependencies
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

## Quick Start

### 1. Setup Your Profile

**Option A: Interactive Setup (Recommended)**

```bash
python setup_profile.py
```

**Option B: Manual Setup**

Edit `example_usage.py` to add your information:

```python
from src.profile_manager import ProfileManager

profile = ProfileManager()

# Add your personal info
profile.update_personal_info(
    first_name="Your Name",
    last_name="Last Name",
    email="your.email@university.edu",
    phone="(555) 123-4567",
    linkedin="https://linkedin.com/in/yourprofile",
    github="https://github.com/yourusername"
)

# Add education
profile.add_education(
    school="Your University",
    degree="Bachelor of Science",
    major="Computer Science",
    gpa=3.8,
    start_date="2022-09",
    end_date="2026-05"
)

# Add experience, projects, skills, etc.
profile.save_profile()
```

### 2. Apply to an Internship

**NEW: Simple CLI Interface**

Just run:

```bash
python apply.py
```

The bot will:
1. Ask for the internship application URL
2. Detect if account creation is needed
3. Automatically create username/password
4. Fill out the entire application form
5. Take screenshots for your review

**Advanced: Programmatic Usage**

```python
import asyncio
from src.profile_manager import ProfileManager
from src.application_bot import InternshipApplicationBot

async def main():
    profile = ProfileManager()
    bot = InternshipApplicationBot(profile, headless=False)

    await bot.start()

    result = await bot.apply_to_job(
        company="Google",
        position="Software Engineering Intern",
        url="https://careers.google.com/jobs/...",
        submit=False  # Set True to actually submit
    )

    await bot.close()

asyncio.run(main())
```

### 3. Batch Apply to Multiple Jobs

```python
jobs = [
    {
        "company": "Google",
        "position": "SWE Intern",
        "url": "https://careers.google.com/..."
    },
    {
        "company": "Meta",
        "position": "Software Engineer Intern",
        "url": "https://metacareers.com/..."
    }
]

results = await bot.apply_to_multiple_jobs(
    job_list=jobs,
    submit=False,
    delay=5000  # Wait 5s between applications
)
```

## How It Works

1. **Profile Management**: Stores your information in structured JSON format
2. **Navigation**: Uses Playwright to navigate to application pages
3. **Account Detection**: Automatically detects login/signup pages
4. **Account Creation**: Generates secure username/password and creates accounts
5. **Credential Storage**: Saves credentials securely in your profile for future use
6. **Form Detection**: Scans the page for input fields, textareas, and selects
7. **Smart Matching**: Matches form fields to your profile data using pattern recognition
8. **Auto-Fill**: Fills detected fields with appropriate information
9. **Review**: Takes screenshots for manual review
10. **Tracking**: Logs all applications to CSV for tracking

## Features in Detail

### Account Creation

The bot automatically:
- **Detects** if you need to create an account or login
- **Generates** secure username (based on your name + random suffix)
- **Creates** strong passwords (16 characters, meets all requirements)
- **Stores** credentials in your profile for future logins
- **Reuses** credentials when you apply to the same company again

### Field Detection

The bot automatically detects and fills common fields:

- **Account**: Username, password, email verification
- **Personal**: First name, last name, email, phone, address
- **Education**: University, degree, major, GPA, graduation date
- **Professional**: LinkedIn, GitHub, portfolio
- **Documents**: Resume, cover letter, transcript uploads
- **Experience**: Work history, projects, skills

## Preview Mode

By default, the bot runs in **preview mode** (`submit=False`):
- Fills out forms
- Takes screenshots
- Does NOT click submit
- Allows you to review before actual submission

Set `submit=True` only when you're confident the bot is working correctly.

## Application Tracking

All applications are tracked in `data/applications.csv`:

```python
# Get statistics
stats = bot.get_statistics()
print(f"Total: {stats['total_applications']}")
print(f"Success rate: {stats['success_rate']}%")

# Get recent applications
recent = bot.get_recent_applications(limit=10)
print(recent)
```

## Screenshots

Screenshots are automatically saved at:
- `data/screenshots/{application_id}_initial.png` - Before filling
- `data/screenshots/{application_id}_filled.png` - After filling
- `data/screenshots/{application_id}_error.png` - If error occurs

## Limitations & Considerations

### Current Limitations
- **CAPTCHAs**: Cannot handle CAPTCHAs (requires manual intervention)
- **Custom Questions**: Doesn't answer open-ended questions yet (needs AI integration)
- **Complex Forms**: May struggle with unusual form layouts
- **Rate Limiting**: Some sites may block rapid applications

### Best Practices
- Always run in preview mode first
- Review screenshots before enabling submit
- Don't spam applications - space them out
- Customize responses for each company
- Check Terms of Service for automation policies

### Legal & Ethical
- Only use for legitimate applications
- Don't submit false information
- Respect site Terms of Service
- Some platforms explicitly prohibit automation

## Future Enhancements

- [ ] AI integration for answering custom questions (Claude/GPT)
- [ ] CAPTCHA solving (manual intervention workflow)
- [ ] Multi-page application support
- [ ] Custom field mapping configuration
- [ ] Email confirmation tracking
- [ ] Browser session persistence
- [ ] Proxy support for rate limiting

## Troubleshooting

### "File not found" errors
Make sure to create the `data/` and `data/screenshots/` directories:
```bash
mkdir -p data/screenshots
```

### Browser not launching
Install Playwright browsers:
```bash
playwright install chromium
```

### Fields not filling
Check the screenshot to see what fields were detected. You may need to customize the field detection patterns in `form_filler.py`.

## Contributing

This is a hackathon project. Feel free to extend and customize for your needs!

## License

MIT License - Use at your own risk. Always verify applications before submission.
