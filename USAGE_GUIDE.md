# Usage Guide - Simple Workflow

## Complete Workflow from Start to Finish

### Step 1: Install Everything

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create data directory
mkdir -p data/screenshots
```

### Step 2: Set Up Your Profile (One Time)

```bash
python setup_profile.py
```

You'll be asked to enter:
- **Personal Info**: Name, email, phone, LinkedIn, GitHub
- **Address**: Street, city, state, ZIP
- **Education**: University, degree, major, GPA, graduation date
- **Experience**: Previous jobs/internships
- **Skills**: Technical skills, languages
- **Documents**: Paths to your resume, cover letter, transcript

**Example:**
```
First Name: John
Last Name: Doe
Email: john.doe@university.edu
Phone: (555) 123-4567
LinkedIn URL: https://linkedin.com/in/johndoe
...
```

### Step 3: Apply to Internships

```bash
python apply.py
```

The bot will ask you:

1. **"Enter the internship application URL:"**
   - Paste the URL of the internship application page
   - Example: `https://careers.google.com/jobs/results/123456789/`

2. **"Company name:"** (optional)
   - Enter the company name or press Enter to skip

3. **"Position/Role:"** (optional)
   - Enter the position or press Enter to skip

4. **"Do you want to actually submit?"**
   - Type `no` for preview mode (recommended first time)
   - Type `yes` to actually submit

### What Happens Next

The bot will:

1. **Open a browser window** (so you can watch)

2. **Navigate to the URL** you provided

3. **Detect the page type**:
   - Login page? → Offers to use stored credentials or create account
   - Signup page? → Offers to auto-create account
   - Application form? → Starts filling directly

4. **Handle account creation** (if needed):
   - Generates secure username: `johndoe1234`
   - Generates secure password: `Xy9$mK2@pL5#hN8!`
   - Fills in all account fields
   - **SAVES CREDENTIALS** to your profile

5. **Fill out the application**:
   - Detects all form fields
   - Matches them to your profile data
   - Fills in everything automatically

6. **Take screenshots**:
   - Before filling: `data/screenshots/{id}_initial.png`
   - After filling: `data/screenshots/{id}_filled.png`

7. **Show results**:
   - Total fields found
   - Fields successfully filled
   - Fields that couldn't be filled (you'll need to fill these manually)

8. **Submit** (only if you said yes):
   - Finds and clicks the submit button
   - Confirms submission

## Example Session

```bash
$ python apply.py

======================================================================
    AI INTERNSHIP APPLICATION BOT
======================================================================

✓ Profile loaded successfully!
  Name: John Doe
  Email: john.doe@university.edu

Enter the internship application URL:
URL: https://www.workday.com/en-us/company/careers/apply-job.html

✓ Application URL: https://www.workday.com/en-us/company/careers/apply-job.html
✓ Domain: www.workday.com

Company name (optional, press Enter to skip): Workday
Position/Role (optional, press Enter to skip): Software Engineering Intern

======================================================================
Starting application to: Software Engineering Intern at Workday
======================================================================

⚠️  PREVIEW MODE: The bot will fill out the form but NOT submit it.
Do you want to actually submit the application? (yes/no): no
✓ PREVIEW MODE - Application will NOT be submitted

🌐 Starting browser...
🔗 Navigating to https://www.workday.com/...

📝 Account creation page detected!
Do you want the bot to automatically create an account? (yes/no): yes

🔐 Detecting account creation form...

✓ Generated credentials:
  Email: john.doe@university.edu
  Username: johndoe7432
  Password: Qw8$eR2@tY5#uI9!

  ✓ Filled email field
  ✓ Filled username field
  ✓ Filled password field 1
  ✓ Filled password field 2
  ✓ Filled first name field
  ✓ Filled last name field

✓ Account creation form filled!

🔑 IMPORTANT - Save these credentials:
   Email: john.doe@university.edu
   Username: johndoe7432
   Password: Qw8$eR2@tY5#uI9!

✓ Credentials saved to profile

======================================================================
FILLING OUT APPLICATION FORM
======================================================================

🤖 Detecting and filling form fields...

📊 Form filling results:
  Total fields detected: 25
  Successfully filled: 22
  Unfilled fields: 3

✓ Filled fields:
    - first_name
    - last_name
    - email
    - phone
    - address
    - city
    - state
    - zip
    - university
    - degree
    - major
    - gpa
    ... and 10 more

⚠️  Unfilled fields (may need manual attention):
    - work_authorization (REQUIRED)
    - cover_letter_text
    - references

📸 Screenshot saved: data/screenshots/app_001_filled.png

======================================================================
PREVIEW MODE - APPLICATION NOT SUBMITTED
======================================================================

The form has been filled out but NOT submitted.
Please review the filled form in the browser.

To submit:
  1. Review all fields carefully
  2. Fill in any missing required fields
  3. Click the submit button manually

Press Enter to close the browser...
```

## Important Notes

### First Time Using the Bot

1. **Always use preview mode first** (`submit=no`)
2. **Review the screenshots** in `data/screenshots/`
3. **Check all filled fields** are correct
4. **Fill in any missing required fields** manually
5. **Only enable submit mode** after you're confident

### Credentials

- Credentials are saved to `data/user_profile.json`
- They're stored by domain (e.g., `workday.com`)
- Next time you apply to the same company, bot will offer to reuse them
- **Keep your profile.json secure** - it contains passwords!

### What the Bot CAN'T Do

- **CAPTCHAs**: You'll need to solve these manually
- **Custom questions**: Open-ended questions like "Why do you want to work here?" need manual answers
- **Multi-page applications**: May need manual navigation between pages
- **Complex validation**: Some sites have unusual validation that may fail

### Privacy & Security

- All data stays on your local machine
- No data is sent to external servers
- Credentials are stored in plain text in `data/user_profile.json`
- **Add `data/` to `.gitignore`** if using version control!

## Tips for Success

1. **Fill out your profile completely** - More data = better auto-fill
2. **Use good file paths** - Provide absolute paths to resume/documents
3. **Watch the browser** - Running in visible mode lets you catch issues
4. **Take your time** - Review before submitting
5. **Test on less important applications first**

## Troubleshooting

### "No profile found"
Run `python setup_profile.py` first

### "Could not find submit button"
The bot looks for common selectors. You may need to click submit manually.

### "Field not filled"
Check if the field is in your profile. Some fields may need manual input.

### Browser doesn't open
Run `playwright install chromium` again

## Need Help?

Check the main README.md for more detailed documentation!
