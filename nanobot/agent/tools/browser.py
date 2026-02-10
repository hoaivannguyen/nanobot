"""Browser automation tool using Playwright."""

from typing import Any
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from loguru import logger

from nanobot.agent.tools.base import Tool


class BrowserTool(Tool):
    """
    Browser automation tool for navigating, clicking, and extracting data.

    Capabilities:
    - Navigate to URLs
    - Click elements
    - Fill forms
    - Extract text/HTML
    - Take screenshots
    """

    name = "browser"
    description = (
        "Automate browser interactions: navigate to URLs, click buttons, "
        "fill forms, extract page content, and take screenshots."
    )
    parameters = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform",
                "enum": ["navigate", "click", "fill", "extract", "screenshot"]
            },
            "url": {
                "type": "string",
                "description": "URL to navigate to (required for 'navigate' action)"
            },
            "selector": {
                "type": "string",
                "description": "CSS selector for element (required for 'click', 'fill', 'extract')"
            },
            "text": {
                "type": "string",
                "description": "Text to fill in form field (required for 'fill' action)"
            },
            "screenshot_path": {
                "type": "string",
                "description": "Path to save screenshot (optional for 'screenshot' action)"
            },
            "wait_timeout": {
                "type": "integer",
                "description": "Timeout in milliseconds (default: 30000)",
                "minimum": 1000,
                "maximum": 60000
            }
        },
        "required": ["action"]
    }

    def __init__(self, headless: bool = True, user_data_dir: str | None = None):
        """
        Initialize browser tool.

        Args:
            headless: Run browser in headless mode (no GUI)
            user_data_dir: Directory to persist cookies/session (for staying logged in)
        """
        self.headless = headless
        self.user_data_dir = user_data_dir
        self._browser = None
        self._context = None
        self._page = None
        self._playwright = None

    async def execute(
        self,
        action: str,
        url: str | None = None,
        selector: str | None = None,
        text: str | None = None,
        screenshot_path: str | None = None,
        wait_timeout: int = 30000,
        **kwargs: Any
    ) -> str:
        """Execute browser automation action."""
        try:
            # Initialize browser if not already running
            if self._browser is None:
                await self._init_browser()

            # Ensure we have a page
            if self._page is None:
                self._page = await self._context.new_page()

            # Execute action
            if action == "navigate":
                if not url:
                    return "Error: 'url' parameter required for navigate action"
                return await self._navigate(url, wait_timeout)

            elif action == "click":
                if not selector:
                    return "Error: 'selector' parameter required for click action"
                return await self._click(selector, wait_timeout)

            elif action == "fill":
                if not selector or text is None:
                    return "Error: 'selector' and 'text' parameters required for fill action"
                return await self._fill(selector, text, wait_timeout)

            elif action == "extract":
                if not selector:
                    return "Error: 'selector' parameter required for extract action"
                return await self._extract(selector, wait_timeout)

            elif action == "screenshot":
                return await self._screenshot(screenshot_path)

            else:
                return f"Error: Unknown action '{action}'"

        except PlaywrightTimeout:
            return f"Error: Timeout waiting for {action} to complete"
        except Exception as e:
            logger.error(f"Browser tool error: {e}")
            return f"Error: {str(e)}"

    async def _init_browser(self) -> None:
        """Initialize Playwright browser."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)

        # Use persistent context for cookies/sessions if user_data_dir is set
        if self.user_data_dir:
            self._context = await self._playwright.chromium.launch_persistent_context(
                self.user_data_dir,
                headless=self.headless,
                # Bypass some bot detection
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            )
            self._page = self._context.pages[0] if self._context.pages else await self._context.new_page()
        else:
            self._context = await self._browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )

        logger.info(f"Browser initialized (persistent: {bool(self.user_data_dir)})")

    async def _navigate(self, url: str, timeout: int) -> str:
        """Navigate to URL."""
        await self._page.goto(url, timeout=timeout)
        title = await self._page.title()
        return f"Navigated to '{title}' ({url})"

    async def _click(self, selector: str, timeout: int) -> str:
        """Click an element."""
        await self._page.click(selector, timeout=timeout)
        return f"Clicked element: {selector}"

    async def _fill(self, selector: str, text: str, timeout: int) -> str:
        """Fill a form field."""
        await self._page.fill(selector, text, timeout=timeout)
        return f"Filled '{selector}' with text"

    async def _extract(self, selector: str, timeout: int) -> str:
        """Extract text from element(s)."""
        await self._page.wait_for_selector(selector, timeout=timeout)
        elements = await self._page.query_selector_all(selector)

        texts = []
        for elem in elements[:10]:  # Limit to 10 elements
            text = await elem.inner_text()
            texts.append(text.strip())

        if not texts:
            return f"No elements found matching: {selector}"

        return f"Extracted {len(texts)} element(s):\n" + "\n---\n".join(texts)

    async def _screenshot(self, path: str | None) -> str:
        """Take a screenshot."""
        path = path or "screenshot.png"
        await self._page.screenshot(path=path)
        return f"Screenshot saved to: {path}"

    async def cleanup(self) -> None:
        """Clean up browser resources."""
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        logger.info("Browser cleaned up")
