from typing import Dict, Any, List
from .browser_automation import BrowserAutomation
from .form_filler import FormFiller
from .application_tracker import ApplicationTracker
from .profile_manager import ProfileManager
import asyncio

# Optional agent import is only used when opt-in
try:
    from .agent import ApplicationAgent
except Exception:
    ApplicationAgent = None


class InternshipApplicationBot:
    """Main bot orchestrator for automated internship applications."""

    def __init__(self, profile_manager: ProfileManager, headless: bool = False,
                 use_agent: bool = False, agent_provider: str = "anthropic"):
        """
        
        Initialize the application bot.

        Args:
            profile_manager: User profile manager with all personal info
            headless: Run browser in headless mode
        """
        self.profile_manager = profile_manager
        self.browser = BrowserAutomation(headless=headless, slow_mo=100)
        self.tracker = ApplicationTracker()
        self.current_application_id = None
        # Create agent if requested
        self.agent = None
        if use_agent:
            if ApplicationAgent is None:
                raise RuntimeError("Agent module not available. Make sure src/agent.py is present and imports succeed.")
            self.agent = ApplicationAgent(self.profile_manager.profile, provider=agent_provider)

    async def start(self):
        """Start the bot and browser."""
        await self.browser.start()

    async def close(self):
        """Close the bot and browser."""
        await self.browser.close()

    async def apply_to_job(self, company: str, position: str, url: str,
                          submit: bool = False) -> Dict[str, Any]:
        """
        Apply to a single job posting.

        Args:
            company: Company name
            position: Position/role title
            url: URL of the application page
            submit: Whether to actually submit (False for preview mode)

        Returns:
            Dictionary with application results
        """
        print(f"\n{'='*60}")
        print(f"Applying to: {position} at {company}")
        print(f"URL: {url}")
        print(f"{'='*60}\n")

        # Track application
        self.current_application_id = self.tracker.add_application(
            company=company,
            position=position,
            url=url,
            status='in_progress'
        )

        try:
            # Navigate to application page
            print("Navigating to application page...")
            await self.browser.navigate(url)
            await self.browser.wait(2000)  # Wait for page to load

            # Take screenshot of initial page
            screenshot_path = f"data/screenshots/{self.current_application_id}_initial.png"
            await self.browser.screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

            # Auto-fill form
            print("\nDetecting and filling form fields...")
            form_filler = FormFiller(self.browser.page, self.profile_manager.profile, agent=self.agent)
            fill_results = await form_filler.auto_fill_form()

            print(f"\nForm filling results:")
            print(f"  Total fields: {fill_results['total_fields']}")
            print(f"  Filled: {fill_results['filled_count']}")
            print(f"  Unfilled: {fill_results['unfilled_count']}")

            if fill_results['filled_fields']:
                print(f"\n  Filled fields: {', '.join(fill_results['filled_fields'][:10])}")

            if fill_results['unfilled_fields']:
                print(f"\n  Unfilled fields:")
                for field in fill_results['unfilled_fields'][:5]:
                    required = " (REQUIRED)" if field.get('required') else ""
                    print(f"    - {field['purpose']}{required}")

            # Take screenshot after filling
            screenshot_path = f"data/screenshots/{self.current_application_id}_filled.png"
            await self.browser.screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")

            # Update tracker with fill results
            self.tracker.update_application(
                self.current_application_id,
                filled_fields=fill_results['filled_count'],
                unfilled_fields=fill_results['unfilled_count']
            )

            # Submit if requested
            if submit:
                await self._submit_application()
                self.tracker.mark_submitted(self.current_application_id)
                print("\n✓ Application submitted successfully!")
            else:
                print("\n⚠ Preview mode - application NOT submitted")
                print("Set submit=True to actually submit the application")

            return {
                'success': True,
                'application_id': self.current_application_id,
                'fill_results': fill_results
            }

        except Exception as e:
            error_msg = str(e)
            print(f"\n✗ Error during application: {error_msg}")

            # Take error screenshot
            try:
                screenshot_path = f"data/screenshots/{self.current_application_id}_error.png"
                await self.browser.screenshot(screenshot_path)
                print(f"Error screenshot saved: {screenshot_path}")
            except:
                pass

            # Mark as failed in tracker
            self.tracker.mark_failed(self.current_application_id, error_msg)

            return {
                'success': False,
                'application_id': self.current_application_id,
                'error': error_msg
            }

    async def _submit_application(self):
        """Find and click the submit button."""
        # Common submit button selectors
        submit_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Submit")',
            'button:has-text("Apply")',
            'button:has-text("Send")',
            'a:has-text("Submit")',
            '[role="button"]:has-text("Submit")'
        ]

        for selector in submit_selectors:
            try:
                element = await self.browser.page.query_selector(selector)
                if element:
                    print(f"Found submit button: {selector}")
                    await element.click()
                    await self.browser.wait(3000)  # Wait for submission
                    return
            except:
                continue

        raise Exception("Could not find submit button")

    async def apply_to_multiple_jobs(self, job_list: List[Dict[str, str]],
                                     submit: bool = False, delay: int = 5000):
        """
        Apply to multiple jobs in sequence.

        Args:
            job_list: List of dicts with 'company', 'position', 'url' keys
            submit: Whether to actually submit applications
            delay: Delay between applications in milliseconds
        """
        results = []

        for i, job in enumerate(job_list):
            print(f"\n\nProcessing job {i+1}/{len(job_list)}...")

            result = await self.apply_to_job(
                company=job['company'],
                position=job['position'],
                url=job['url'],
                submit=submit
            )
            results.append(result)

            # Delay between applications
            if i < len(job_list) - 1:
                print(f"\nWaiting {delay/1000}s before next application...")
                await asyncio.sleep(delay / 1000)

        # Print summary
        print(f"\n\n{'='*60}")
        print("BATCH APPLICATION SUMMARY")
        print(f"{'='*60}")
        successful = sum(1 for r in results if r['success'])
        print(f"Total jobs: {len(job_list)}")
        print(f"Successful: {successful}")
        print(f"Failed: {len(job_list) - successful}")
        print(f"{'='*60}\n")

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """Get application statistics."""
        return self.tracker.get_statistics()

    def get_recent_applications(self, limit: int = 10):
        """Get recent applications."""
        return self.tracker.get_recent_applications(limit)
