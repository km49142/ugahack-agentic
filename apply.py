#!/usr/bin/env python3
"""
Main application script for automated internship applications.
This script asks for the internship URL and handles the entire application process.
"""

import asyncio
from src.profile_manager import ProfileManager
from src.application_bot import InternshipApplicationBot
from urllib.parse import urlparse
import sys


async def apply_to_internship():
    """Main application flow."""

    print("=" * 70)
    print("    AI INTERNSHIP APPLICATION BOT")
    print("=" * 70)
    print()

    # Check if profile exists
    profile = ProfileManager()

    # Check if profile is set up
    if not profile.profile['personal_info']['first_name']:
        print("⚠️  No profile found! Please set up your profile first.")
        print()
        print("Run one of these commands:")
        print("  1. python setup_profile.py     (Interactive setup)")
        print("  2. Edit example_usage.py and run it")
        print()
        sys.exit(1)

    print("✓ Profile loaded successfully!")
    print(f"  Name: {profile.profile['personal_info']['first_name']} {profile.profile['personal_info']['last_name']}")
    print(f"  Email: {profile.profile['personal_info']['email']}")
    print()

    # Get internship URL from user
    print("Enter the internship application URL:")
    url = input("URL: ").strip()

    if not url:
        print("❌ No URL provided. Exiting.")
        sys.exit(1)

    # Validate URL
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            print("❌ Invalid URL. Please include http:// or https://")
            sys.exit(1)
        domain = parsed.netloc
    except Exception as e:
        print(f"❌ Invalid URL: {e}")
        sys.exit(1)

    print()
    print(f"✓ Application URL: {url}")
    print(f"✓ Domain: {domain}")
    print()

    # Optional: Get company and position info
    company = input("Company name (optional, press Enter to skip): ").strip()
    position = input("Position/Role (optional, press Enter to skip): ").strip()

    if not company:
        company = domain.split('.')[0].title()
    if not position:
        position = "Internship"

    print()

    # Ask if user wants to use the AI agent
    use_agent_choice = input("Do you want to use the AI agent to answer questions? (yes/no): ").strip().lower()
    use_agent = use_agent_choice in ['yes', 'y']
    agent_provider = None
    if use_agent:
        provider_choice = input("Which provider do you want to use? (anthropic/tensorflow): ").strip().lower()
        if provider_choice in ["anthropic", "tensorflow"]:
            agent_provider = provider_choice
            print(f"✓ Using {agent_provider} agent.")
        else:
            print("⚠️  Invalid provider. Defaulting to no agent.")
            use_agent = False
    
    print()
    print("=" * 70)
    print(f"Starting application to: {position} at {company}")
    print("=" * 70)
    print()

    # Ask if user wants to actually submit
    print("⚠️  PREVIEW MODE: The bot will fill out the form but NOT submit it.")
    submit_choice = input("Do you want to actually submit the application? (yes/no): ").strip().lower()
    submit = submit_choice in ['yes', 'y']

    if submit:
        print("⚠️  SUBMIT MODE ENABLED - Application will be submitted!")
    else:
        print("✓ PREVIEW MODE - Application will NOT be submitted")

    print()

    # Create bot
    bot = InternshipApplicationBot(profile, headless=False, use_agent=use_agent, agent_provider=agent_provider)

    try:
        # Start browser
        print("🌐 Starting browser...")
        await bot.start()

        # Run the application process
        await bot.apply_to_job(company=company, position=position, url=url, submit=submit)

        print("\n" + "=" * 70)
        print("Press Enter to close the browser...")
        input()

    except Exception as e:
        print(f"\n❌ Error during application: {e}")

        # Take error screenshot
        try:
            screenshot_path = f"data/screenshots/error_{bot.current_application_id}.png"
            await bot.browser.screenshot(screenshot_path)
            print(f"📸 Error screenshot saved: {screenshot_path}")
        except:
            pass

        if bot.current_application_id:
            bot.tracker.mark_failed(bot.current_application_id, str(e))

        print("\nPress Enter to close the browser...")
        input()

    finally:
        # Close browser
        print("\n🔒 Closing browser...")
        await bot.close()
        print("✓ Done!")


if __name__ == "__main__":
    try:
        asyncio.run(apply_to_internship())
    except KeyboardInterrupt:
        print("\n\n⚠️  Application cancelled by user")
        sys.exit(0)
