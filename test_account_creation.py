#!/usr/bin/env python3
"""
Test script to verify account creation functionality.
This doesn't actually create accounts, just tests the detection logic.
"""

import asyncio
from playwright.async_api import async_playwright


async def _test_account_detection_async():
    """Test account creation detection on sample pages."""

    print("=" * 60)
    print("Testing Account Creation Detection")
    print("=" * 60)
    print()

    # Sample test URLs (these are real login/signup pages for testing)
    test_cases = [
        {
            "name": "Workday Signup",
            "url": "https://myworkdayjobs.com",
            "expected": "login or signup"
        },
        {
            "name": "LinkedIn Login",
            "url": "https://www.linkedin.com/login",
            "expected": "login"
        }
    ]

    playwright = await async_playwright().start()
    try:
        browser = await playwright.chromium.launch(headless=True)
    except Exception as e:
        print(f"⚠️  Could not launch browser: {e}")
        print("Please run: playwright install chromium")
        await playwright.stop()
        return

    context = await browser.new_context()
    page = await context.new_page()

    try:
        for test in test_cases:
            print(f"Testing: {test['name']}")
            print(f"URL: {test['url']}")

            try:
                await page.goto(test['url'], timeout=10000)
                await page.wait_for_timeout(2000)

                # Check for signup/login indicators
                page_text = await page.inner_text('body')
                page_text_lower = page_text.lower()

                has_login = 'login' in page_text_lower or 'sign in' in page_text_lower
                has_signup = 'sign up' in page_text_lower or 'create account' in page_text_lower
                has_password = await page.query_selector('input[type="password"]')

                print(f"  Has login text: {has_login}")
                print(f"  Has signup text: {has_signup}")
                print(f"  Has password field: {has_password is not None}")
                print(f"  ✓ Page loaded successfully")

            except Exception as e:
                print(f"  ✗ Error: {e}")

            print()

        print("=" * 60)
        print("Test complete!")
        
        # Only wait for input if running as __main__ and not in a CI environment
        import os
        if __name__ == "__main__" and not os.environ.get('CI'):
            print("Press Enter to close...")
            input()

    finally:
        await browser.close()
        await playwright.stop()


def test_account_detection():
    """Synchronous wrapper so pytest can run the async test."""
    asyncio.run(_test_account_detection_async())


if __name__ == "__main__":
    asyncio.run(_test_account_detection_async())
