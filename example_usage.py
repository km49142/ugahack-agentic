import asyncio
from src.profile_manager import ProfileManager
from src.application_bot import InternshipApplicationBot


async def setup_profile():
    """
    DEPRECATED: Use setup_profile.py instead or just load existing profile.
    This function now just loads the existing profile without overwriting it.
    """
    profile = ProfileManager()

    print("=" * 60)
    print("⚠️  WARNING: This example file uses the existing profile.")
    print("To create a new profile, run: python setup_profile.py")
    print("To apply to jobs, run: python apply.py")
    print("=" * 60)
    print()
    print("Profile loaded:")
    print(profile.get_profile_summary())

    return profile


async def example_single_application():
    """Example: Apply to a single job."""
    # Setup profile
    profile = await setup_profile()

    # Create bot
    bot = InternshipApplicationBot(profile, headless=False, use_agent=True)

    try:
        # Start browser
        await bot.start()

        # Apply to job (set submit=True to actually submit)
        result = await bot.apply_to_job(
            company="Google",
            position="Software Engineering Intern",
            url="https://careers.google.com/jobs/...",  # Replace with actual URL
            submit=False  # Set to True to actually submit
        )

        print("\nApplication result:", result)

    finally:
        # Close browser
        await bot.close()


async def example_batch_applications():
    """Example: Apply to multiple jobs."""
    # Setup profile
    profile = await setup_profile()

    # List of jobs to apply to
    jobs = [
        {
            "company": "Google",
            "position": "Software Engineering Intern",
            "url": "https://careers.google.com/jobs/..."
        },
        {
            "company": "Meta",
            "position": "Software Engineer Intern",
            "url": "https://www.metacareers.com/jobs/..."
        },
        {
            "company": "Amazon",
            "position": "SDE Intern",
            "url": "https://www.amazon.jobs/..."
        }
    ]

    # Create bot
    bot = InternshipApplicationBot(profile, headless=False, use_agent=True)

    try:
        # Start browser
        await bot.start()

        # Apply to all jobs
        results = await bot.apply_to_multiple_jobs(
            job_list=jobs,
            submit=False,  # Set to True to actually submit
            delay=5000  # 5 seconds between applications
        )

        # Print statistics
        stats = bot.get_statistics()
        print("\nApplication Statistics:")
        print(f"Total applications: {stats['total_applications']}")
        print(f"Submitted: {stats['submitted']}")
        print(f"Pending: {stats['pending']}")
        print(f"Failed: {stats['failed']}")

    finally:
        # Close browser
        await bot.close()


async def example_with_custom_answers():
    """Example: Using custom answers for specific questions."""
    # This would require AI integration (Claude/GPT) for answering custom questions
    # For now, this is a placeholder showing the structure
    pass


if __name__ == "__main__":
    # Run single application example
    asyncio.run(example_single_application())

    # Or run batch applications
    # asyncio.run(example_batch_applications())
