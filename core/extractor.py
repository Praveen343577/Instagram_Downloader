from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from config import (
    TARGET_URL,
    INPUT_SELECTOR,
    SUBMIT_SELECTOR,
    RESULT_CONTAINER_SELECTOR,
    ERROR_CONTAINER_SELECTOR,
    GRID_SELECTOR,
    ACCOUNT_NAME_SELECTOR,
    DESCRIPTION_SELECTOR,
    DOWNLOAD_LINK_SELECTOR,
    RESOLUTION_HIERARCHY,
    STATUS_SUCCESS,
    STATUS_DEADLINK,
    STATUS_FAILED
)

def extract_media(page: Page, url: str) -> dict:
    """
    Injects the URL, triggers the extraction, and parses the DOM for the highest quality media.
    Evaluates individual items within a carousel/grid to ensure all nodes are captured.
    """
    try:
        page.goto(TARGET_URL, wait_until="domcontentloaded")
        
        # Inject URL and submit
        page.fill(INPUT_SELECTOR, url)
        page.click(SUBMIT_SELECTOR)
        
        # Race condition: wait for either result or error container to become visible
        selector = f"{RESULT_CONTAINER_SELECTOR}:visible, {ERROR_CONTAINER_SELECTOR}:visible"
        page.wait_for_selector(selector, timeout=30000)
        
        if page.locator(ERROR_CONTAINER_SELECTOR).is_visible():
            return {
                "status": STATUS_DEADLINK,
                "account_name": None,
                "description": None,
                "download_urls": []
            }
            
        # Extract Metadata
        account_name = None
        description = None
        
        acc_locator = page.locator(ACCOUNT_NAME_SELECTOR)
        if acc_locator.count() > 0:
            account_name = acc_locator.first.inner_text().strip()
            
        desc_locator = page.locator(DESCRIPTION_SELECTOR)
        if desc_locator.count() > 0:
            description = desc_locator.first.inner_text().strip()
            
        # Extract highest quality media from grid
        download_urls = []
        grid_items = page.locator(GRID_SELECTOR).locator("> div").all()
        
        # Fallback if the layout doesn't use the grid role (e.g. single profile picture)
        if not grid_items:
            grid_items = [page.locator(RESULT_CONTAINER_SELECTOR)]
            
        for item in grid_items:
            best_link = None
            best_rank = len(RESOLUTION_HIERARCHY)
            
            a_tags = item.locator(DOWNLOAD_LINK_SELECTOR).all()
            for a in a_tags:
                href = a.get_attribute("href")
                if not href:
                    continue
                    
                text_content = a.inner_text()
                
                # Evaluate quality rank against the hierarchy list
                for rank, resolution in enumerate(RESOLUTION_HIERARCHY):
                    if resolution in text_content and rank < best_rank:
                        best_rank = rank
                        best_link = href
                        break
                
                # Fallback if no text matches but a download link exists
                if not best_link and rank == len(RESOLUTION_HIERARCHY) - 1 and best_rank == len(RESOLUTION_HIERARCHY):
                    best_link = href
                        
            if best_link:
                download_urls.append(best_link)
                
        if not download_urls:
            return {
                "status": STATUS_FAILED,
                "account_name": account_name,
                "description": description,
                "download_urls": []
            }
            
        return {
            "status": STATUS_SUCCESS,
            "account_name": account_name,
            "description": description,
            "download_urls": download_urls
        }
        
    except PlaywrightTimeoutError:
        return {
            "status": STATUS_FAILED,
            "account_name": None,
            "description": None,
            "download_urls": []
        }
    except Exception:
        return {
            "status": STATUS_FAILED,
            "account_name": None,
            "description": None,
            "download_urls": []
        }