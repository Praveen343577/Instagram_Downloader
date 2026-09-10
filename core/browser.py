import os
from playwright.sync_api import Playwright, BrowserContext, Page
from playwright_stealth import Stealth

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "browser_session")

def init_browser(playwright: Playwright) -> tuple[BrowserContext, Page]:
    """
    Initializes a persistent, headless Chromium context with stealth evasion.
    To be called within a Playwright context manager in main.py.
    """
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=True,
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars"
        ]
    )
    
    # Persistent contexts spawn with an initial blank page
    page = context.pages[0] if context.pages else context.new_page()
    
    # Apply anti-bot evasions (WebDriver flag removal, navigator spoofing)
    Stealth().apply_stealth_sync(page)
    
    return context, page