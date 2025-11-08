#!/usr/bin/env python3
"""
Main application script for automated internship applications.
This script asks for the internship URL and handles the entire application process.
"""

import asyncio
from src.profile_manager import ProfileManager
from src.application_bot import InternshipApplicationBot
from src.account_creator import AccountCreator
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

    # Create bot (visible browser for user to watch)
    bot = InternshipApplicationBot(profile, headless=False)

    try:
        # Start browser
        print("🌐 Starting browser...")
        await bot.start()

        # Navigate to URL
        print(f"🔗 Navigating to {url}...")
        await bot.browser.navigate(url)
        await bot.browser.wait(3000)

        # Create account creator
        account_creator = AccountCreator(bot.browser.page, profile.profile)

        # Check if we're on a login page
        is_login = await account_creator.detect_login_page()
        is_signup = await account_creator.detect_account_creation_page()

        if is_login:
            print("\n🔐 Login page detected!")

            # Check if we have stored credentials for this domain
            if domain in profile.profile.get('credentials', {}):
                print(f"✓ Found stored credentials for {domain}")
                choice = input("Do you want to use stored credentials? (yes/no): ").strip().lower()

                if choice in ['yes', 'y']:
                    # Login with stored credentials
                    login_result = await account_creator.login_with_credentials(domain)

                    if login_result['success']:
                        print("✓ Credentials filled!")

                        # Look for login button
                        login_btn = await bot.browser.page.query_selector('button[type="submit"]')
                        if not login_btn:
                            login_btn = await bot.browser.page.query_selector('button:has-text("Log in")')
                        if not login_btn:
                            login_btn = await bot.browser.page.query_selector('button:has-text("Sign in")')

                        if login_btn:
                            print("🔘 Clicking login button...")
                            await login_btn.click()
                            await bot.browser.wait(3000)
                        else:
                            print("⚠️  Could not find login button. Please login manually and press Enter to continue...")
                            input()
                else:
                    print("⚠️  Please login manually and press Enter to continue...")
                    input()
            else:
                # Check if there's a "Create Account" link
                print("\n🔍 Looking for 'Create Account' option...")
                create_account_links = await bot.browser.page.query_selector_all('a:has-text("Create Account"), a:has-text("Sign Up"), a:has-text("Register")')

                if create_account_links:
                    print("✓ Found 'Create Account' link")
                    choice = input("Do you want to create a new account? (yes/no): ").strip().lower()

                    if choice in ['yes', 'y']:
                        print("🔘 Clicking 'Create Account'...")
                        await create_account_links[0].click()
                        await bot.browser.wait(3000)
                        is_signup = True
                    else:
                        print("⚠️  Please login or create account manually and press Enter to continue...")
                        input()
                else:
                    print("⚠️  Please login manually and press Enter to continue...")
                    input()

        if is_signup:
            print("\n📝 Account creation page detected!")
            choice = input("Do you want the bot to automatically create an account? (yes/no): ").strip().lower()

            if choice in ['yes', 'y']:
                # Create account
                account_result = await account_creator.create_account()

                if account_result['success']:
                    print(f"\n✓ Account creation form filled!")
                    print(f"\n🔑 IMPORTANT - Save these credentials:")
                    print(f"   Email: {account_result['email']}")
                    print(f"   Username: {account_result['username']}")
                    print(f"   Password: {account_result['password']}")
                    print()

                    # Save credentials to profile
                    profile.save_profile()
                    print("✓ Credentials saved to profile")

                    # Look for create account button
                    create_btn = await account_creator.find_create_account_button()

                    if create_btn:
                        print("\n🔘 Found account creation button")
                        choice = input("Click the button to create account? (yes/no): ").strip().lower()

                        if choice in ['yes', 'y']:
                            await create_btn.click()
                            await bot.browser.wait(3000)
                            print("✓ Account creation button clicked!")
                    else:
                        print("\n⚠️  Could not find 'Create Account' button.")
                        print("Please click it manually and press Enter to continue...")
                        input()
                else:
                    print(f"\n❌ Failed to create account: {account_result.get('error')}")
                    print("Please create account manually and press Enter to continue...")
                    input()
            else:
                print("⚠️  Please create account manually and press Enter to continue...")
                input()

        # Now fill out the application form
        print("\n" + "=" * 70)
        print("FILLING OUT APPLICATION FORM")
        print("=" * 70)
        print()

        # Wait a bit for any redirects
        await bot.browser.wait(2000)

        # Look for "Apply Now" button
        print("🔍 Looking for 'Apply Now' button...")
        apply_button_selectors = [
            'button:has-text("Apply now")',
            'button:has-text("Apply Now")',
            'a:has-text("Apply now")',
            'a:has-text("Apply Now")',
            'button:has-text("Apply")',
            'a:has-text("Apply")',
            '[class*="apply"]:has-text("Apply")',
            'button[class*="apply-button"]',
            'a[class*="apply-button"]'
        ]

        apply_button_found = False
        for selector in apply_button_selectors:
            try:
                button = await bot.browser.page.query_selector(selector)
                if button:
                    # Check if button is visible
                    is_visible = await button.is_visible()
                    if is_visible:
                        print(f"✓ Found 'Apply Now' button: {selector}")
                        await button.click()
                        apply_button_found = True
                        print("🔘 Clicked 'Apply Now' button")
                        await bot.browser.wait(2000)  # Wait for dropdown to appear
                        break
            except Exception as e:
                continue

        if not apply_button_found:
            print("⚠️  No 'Apply Now' button found - assuming already on application form")

        # Check if there's a dropdown menu that appeared
        if apply_button_found:
            print("🔍 Checking for dropdown menu options...")
            await bot.browser.wait(1000)  # Give dropdown time to render

            dropdown_selectors = [
                'a:has-text("Apply Now")',
                'li:has-text("Apply Now") a',
                'button:has-text("Apply Now")',
                '[class*="dropdown"] a:has-text("Apply")',
                '[role="menuitem"]:has-text("Apply Now")',
                'a[href*="apply"]'
            ]

            dropdown_clicked = False
            for selector in dropdown_selectors:
                try:
                    # Look for all matching elements since there might be multiple
                    elements = await bot.browser.page.query_selector_all(selector)
                    for element in elements:
                        is_visible = await element.is_visible()
                        text = await element.inner_text()

                        # Make sure it's the "Apply Now" option, not "Start apply with LinkedIn"
                        if is_visible and "Apply Now" in text and "LinkedIn" not in text:
                            print(f"✓ Found dropdown 'Apply Now' option")
                            await element.click()
                            dropdown_clicked = True
                            print("🔘 Clicked 'Apply Now' from dropdown")
                            await bot.browser.wait(5000)  # Wait for application form to load
                            break
                except Exception as e:
                    continue

                if dropdown_clicked:
                    break

            if not dropdown_clicked:
                print("⚠️  No dropdown option found - form may have loaded directly")
                await bot.browser.wait(2000)

        # Track the application
        bot.current_application_id = bot.tracker.add_application(
            company=company,
            position=position,
            url=url,
            status='in_progress'
        )

        # Take initial screenshot
        screenshot_path = f"data/screenshots/{bot.current_application_id}_initial.png"
        await bot.browser.screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

        # Auto-fill the form
        from src.form_filler import FormFiller

        print("\n🤖 Detecting and filling form fields...")
        print("   (You'll be asked to answer yes/no questions as they appear)\n")
        form_filler = FormFiller(bot.browser.page, profile.profile)
        fill_results = await form_filler.auto_fill_form(interactive=True)

        print(f"\n📊 Form filling results:")
        print(f"  Total fields detected: {fill_results['total_fields']}")
        print(f"  Auto-filled: {fill_results['filled_count']}")
        print(f"  You answered: {fill_results.get('user_answered_count', 0)}")
        print(f"  Skipped (optional): {fill_results.get('skipped_count', 0)}")
        print(f"  Unfilled fields: {fill_results['unfilled_count']}")

        if fill_results['filled_fields']:
            print(f"\n✓ Auto-filled fields:")
            for field in fill_results['filled_fields'][:10]:
                print(f"    - {field}")
            if len(fill_results['filled_fields']) > 10:
                print(f"    ... and {len(fill_results['filled_fields']) - 10} more")

        if fill_results.get('user_answered_fields'):
            print(f"\n✓ Questions you answered:")
            for field in fill_results['user_answered_fields']:
                print(f"    - {field}")

        if fill_results.get('skipped_fields'):
            print(f"\n⏭️  Skipped optional fields (left blank):")
            for field in fill_results['skipped_fields'][:10]:
                print(f"    - {field}")
            if len(fill_results['skipped_fields']) > 10:
                print(f"    ... and {len(fill_results['skipped_fields']) - 10} more")

        if fill_results['unfilled_fields']:
            print(f"\n⚠️  Unfilled fields (may need manual attention):")
            for field in fill_results['unfilled_fields'][:10]:
                required = " (REQUIRED)" if field.get('required') else ""
                print(f"    - {field['purpose']}{required}")
            if len(fill_results['unfilled_fields']) > 10:
                print(f"    ... and {len(fill_results['unfilled_fields']) - 10} more")

        # Take filled screenshot
        screenshot_path = f"data/screenshots/{bot.current_application_id}_filled.png"
        await bot.browser.screenshot(screenshot_path)
        print(f"\n📸 Screenshot saved: {screenshot_path}")

        # Update tracker
        bot.tracker.update_application(
            bot.current_application_id,
            filled_fields=fill_results['filled_count'],
            unfilled_fields=fill_results['unfilled_count']
        )

        # Submit if requested
        print("\n" + "=" * 70)
        if submit:
            print("⚠️  SUBMITTING APPLICATION...")
            print("=" * 70)

            final_confirm = input("\nAre you sure you want to submit? (yes/no): ").strip().lower()

            if final_confirm in ['yes', 'y']:
                try:
                    await bot._submit_application()
                    bot.tracker.mark_submitted(bot.current_application_id)
                    print("\n✓✓✓ APPLICATION SUBMITTED SUCCESSFULLY! ✓✓✓")
                except Exception as e:
                    print(f"\n❌ Failed to submit: {e}")
                    print("Please submit manually if needed.")
            else:
                print("\n⚠️  Submission cancelled by user")
        else:
            print("PREVIEW MODE - APPLICATION NOT SUBMITTED")
            print("=" * 70)
            print("\nThe form has been filled out but NOT submitted.")
            print("Please review the filled form in the browser.")
            print("\nTo submit:")
            print("  1. Review all fields carefully")
            print("  2. Fill in any missing required fields")
            print("  3. Click the submit button manually")

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
