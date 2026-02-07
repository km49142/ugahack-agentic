from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from typing import Optional, Dict, Any, List
import asyncio


class BrowserAutomation:
    """Core browser automation using Playwright."""

    def __init__(self, headless: bool = False, slow_mo: int = 100):
        """
        Initialize browser automation.

        Args:
            headless: Run browser in headless mode
            slow_mo: Slow down operations by specified milliseconds (useful for debugging)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None

    async def start(self):
        """Start the browser."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await self.context.new_page()

    async def close(self):
        """Close the browser."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def navigate(self, url: str, wait_until: str = "domcontentloaded", timeout: int = 60000):
        """Navigate to a URL."""
        await self.page.goto(url, wait_until=wait_until, timeout=timeout)

    async def screenshot(self, path: str):
        """Take a screenshot."""
        await self.page.screenshot(path=path)

    async def get_page_title(self) -> str:
        """Get the current page title."""
        return await self.page.title()

    async def wait_for_selector(self, selector: str, timeout: int = 30000):
        """Wait for an element to appear."""
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def click(self, selector: str):
        """Click an element."""
        await self.page.click(selector)

    async def fill_text(self, selector: str, text: str):
        """Fill text into an input field."""
        await self.page.fill(selector, text)

    async def select_option(self, selector: str, value: str):
        """Select an option from a dropdown."""
        await self.page.select_option(selector, value)

    async def upload_file(self, selector: str, file_path: str):
        """Upload a file."""
        await self.page.set_input_files(selector, file_path)

    async def execute_script(self, script: str) -> Any:
        """Execute JavaScript on the page."""
        return await self.page.evaluate(script)

    async def get_current_url(self) -> str:
        """Get the current URL."""
        return self.page.url

    async def press_key(self, key: str):
        """Press a keyboard key."""
        await self.page.keyboard.press(key)

    async def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    async def wait(self, milliseconds: int):
        """Wait for a specified time."""
        await self.page.wait_for_timeout(milliseconds)
