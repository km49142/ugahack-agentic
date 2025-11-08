#!/usr/bin/env python3
"""
Test script to verify all components are working correctly.
Run this after installing dependencies to validate setup.
"""

import sys
from pathlib import Path


def test_imports():
    """Test that all required libraries can be imported."""
    print("Testing imports...")

    try:
        import playwright
        print("✓ Playwright")
    except ImportError:
        print("✗ Playwright - Run: pip install playwright")
        return False

    try:
        import docx
        print("✓ python-docx")
    except ImportError:
        print("✗ python-docx - Run: pip install python-docx")
        return False

    try:
        import PyPDF2
        print("✓ PyPDF2")
    except ImportError:
        print("✗ PyPDF2 - Run: pip install PyPDF2")
        return False

    try:
        import pandas
        print("✓ pandas")
    except ImportError:
        print("✗ pandas - Run: pip install pandas")
        return False

    try:
        import httpx
        print("✓ httpx")
    except ImportError:
        print("✗ httpx - Run: pip install httpx")
        return False

    return True


def test_modules():
    """Test that all custom modules can be imported."""
    print("\nTesting custom modules...")

    try:
        from src.profile_manager import ProfileManager
        print("✓ ProfileManager")
    except ImportError as e:
        print(f"✗ ProfileManager: {e}")
        return False

    try:
        from src.resume_parser import ResumeParser
        print("✓ ResumeParser")
    except ImportError as e:
        print(f"✗ ResumeParser: {e}")
        return False

    try:
        from src.browser_automation import BrowserAutomation
        print("✓ BrowserAutomation")
    except ImportError as e:
        print(f"✗ BrowserAutomation: {e}")
        return False

    try:
        from src.form_filler import FormFiller, FormDetector
        print("✓ FormFiller & FormDetector")
    except ImportError as e:
        print(f"✗ FormFiller: {e}")
        return False

    try:
        from src.application_tracker import ApplicationTracker
        print("✓ ApplicationTracker")
    except ImportError as e:
        print(f"✗ ApplicationTracker: {e}")
        return False

    try:
        from src.application_bot import InternshipApplicationBot
        print("✓ InternshipApplicationBot")
    except ImportError as e:
        print(f"✗ InternshipApplicationBot: {e}")
        return False

    return True


def test_profile_manager():
    """Test ProfileManager functionality."""
    print("\nTesting ProfileManager...")

    try:
        from src.profile_manager import ProfileManager

        # Create test profile
        profile = ProfileManager(profile_path="data/test_profile.json")
        profile.update_personal_info(
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )

        # Verify data
        assert profile.profile['personal_info']['first_name'] == "Test"
        assert profile.profile['personal_info']['email'] == "test@example.com"

        print("✓ ProfileManager working correctly")

        # Clean up
        Path("data/test_profile.json").unlink(missing_ok=True)
        return True

    except Exception as e:
        print(f"✗ ProfileManager test failed: {e}")
        return False


def test_application_tracker():
    """Test ApplicationTracker functionality."""
    print("\nTesting ApplicationTracker...")

    try:
        from src.application_tracker import ApplicationTracker

        # Create test tracker
        tracker = ApplicationTracker(db_path="data/test_applications.csv")

        # Add test application
        app_id = tracker.add_application(
            company="Test Corp",
            position="Test Intern",
            url="https://example.com",
            status="pending"
        )

        # Verify
        stats = tracker.get_statistics()
        assert stats['total_applications'] == 1

        print("✓ ApplicationTracker working correctly")

        # Clean up
        Path("data/test_applications.csv").unlink(missing_ok=True)
        return True

    except Exception as e:
        print(f"✗ ApplicationTracker test failed: {e}")
        return False


def test_directories():
    """Test that required directories exist."""
    print("\nChecking directories...")

    data_dir = Path("data")
    screenshots_dir = Path("data/screenshots")

    if not data_dir.exists():
        print("Creating data/ directory...")
        data_dir.mkdir(parents=True)

    if not screenshots_dir.exists():
        print("Creating data/screenshots/ directory...")
        screenshots_dir.mkdir(parents=True)

    print("✓ Required directories exist")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Internship Application Bot - Setup Test")
    print("=" * 60)

    tests = [
        ("Import Test", test_imports),
        ("Module Test", test_modules),
        ("Directory Test", test_directories),
        ("ProfileManager Test", test_profile_manager),
        ("ApplicationTracker Test", test_application_tracker),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{'=' * 60}")
        result = test_func()
        results.append((name, result))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n✅ All tests passed! You're ready to use the bot.")
        print("\nNext steps:")
        print("1. Run 'python setup_profile.py' to configure your profile")
        print("2. Run 'python example_usage.py' to see usage examples")
        print("3. Install Playwright browsers: 'playwright install chromium'")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Install Playwright browsers: playwright install chromium")
        return 1


if __name__ == "__main__":
    sys.exit(main())
