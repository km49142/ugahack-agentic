#!/usr/bin/env python3
"""
Quick setup script to configure your user profile.
Run this first before using the application bot.
"""

from src.profile_manager import ProfileManager


def setup_profile():
    """Interactive profile setup."""
    print("=" * 60)
    print("Internship Application Bot - Profile Setup")
    print("=" * 60)

    profile = ProfileManager()

    # Personal Information
    print("\n📋 Personal Information")
    print("-" * 60)
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    linkedin = input("LinkedIn URL (optional): ").strip()
    github = input("GitHub URL (optional): ").strip()
    portfolio = input("Portfolio URL (optional): ").strip()

    profile.update_personal_info(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        linkedin=linkedin or "",
        github=github or "",
        portfolio=portfolio or ""
    )

    # Address
    print("\n🏠 Address")
    print("-" * 60)
    street = input("Street: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip()
    zip_code = input("ZIP Code: ").strip()
    country = input("Country (default: USA): ").strip() or "USA"

    profile.profile['personal_info']['address'] = {
        "street": street,
        "city": city,
        "state": state,
        "zip": zip_code,
        "country": country
    }

    # Education
    print("\n🎓 Education")
    print("-" * 60)
    add_edu = input("Add education? (y/n): ").lower() == 'y'

    while add_edu:
        school = input("School/University: ").strip()
        degree = input("Degree (e.g., Bachelor of Science): ").strip()
        major = input("Major: ").strip()
        gpa = input("GPA: ").strip()
        start_date = input("Start Date (YYYY-MM): ").strip()
        end_date = input("End Date (YYYY-MM): ").strip()

        profile.add_education(
            school=school,
            degree=degree,
            major=major,
            gpa=float(gpa) if gpa else 0.0,
            start_date=start_date,
            end_date=end_date
        )

        add_edu = input("Add another education entry? (y/n): ").lower() == 'y'

    # Experience
    print("\n💼 Work Experience")
    print("-" * 60)
    add_exp = input("Add work experience? (y/n): ").lower() == 'y'

    while add_exp:
        company = input("Company: ").strip()
        title = input("Job Title: ").strip()
        start_date = input("Start Date (YYYY-MM): ").strip()
        end_date = input("End Date (YYYY-MM or 'Present'): ").strip()
        description = input("Brief Description: ").strip()

        profile.add_experience(
            company=company,
            title=title,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        add_exp = input("Add another experience entry? (y/n): ").lower() == 'y'

    # Skills
    print("\n💡 Skills")
    print("-" * 60)
    technical = input("Technical Skills (comma-separated): ").strip()
    languages = input("Languages (comma-separated): ").strip()

    profile.profile['skills'] = {
        "technical": [s.strip() for s in technical.split(',') if s.strip()],
        "languages": [s.strip() for s in languages.split(',') if s.strip()],
        "soft_skills": []
    }

    # Documents
    print("\n📄 Documents")
    print("-" * 60)
    resume_path = input("Resume file path (leave blank if none): ").strip()
    cover_letter = input("Cover letter file path (leave blank if none): ").strip()
    transcript = input("Transcript file path (leave blank if none): ").strip()

    profile.profile['documents'] = {
        "resume_path": resume_path,
        "cover_letter_template": cover_letter,
        "transcript_path": transcript
    }

    # Save
    profile.save_profile()

    print("\n" + "=" * 60)
    print("✅ Profile saved successfully!")
    print("=" * 60)
    print("\nProfile Summary:")
    print(profile.get_profile_summary())
    print("\nYou can now use the application bot!")
    print("Run: python example_usage.py")


if __name__ == "__main__":
    setup_profile()
