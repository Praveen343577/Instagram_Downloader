import os
import time
import random
from playwright.sync_api import sync_playwright

from config import (
    LINKS_FILE,
    FAILED_FILE,
    DELAY_MIN,
    DELAY_MAX,
    STATUS_SUCCESS,
    STATUS_FAILED,
    STATUS_DEADLINK
)
from db.database import init_db, is_downloaded, insert_record
from utils.sanitizer import sanitize_link
from core.browser import init_browser
from core.extractor import extract_media
from core.downloader import download_files

def record_failure(url: str):
    """Appends a failed or unresolvable URL to failed.txt."""
    os.makedirs(os.path.dirname(FAILED_FILE), exist_ok=True)
    with open(FAILED_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}\n")

def run():
    init_db()

    if not os.path.exists(LINKS_FILE):
        return

    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        raw_links = [line.strip() for line in f if line.strip()]

    with sync_playwright() as playwright:
        context, page = init_browser(playwright)

        try:
            for raw_url in raw_links:
                url = sanitize_link(raw_url)
                if not url:
                    continue

                if is_downloaded(url):
                    continue

                extraction_result = extract_media(page, url)
                status = extraction_result["status"]
                account_name = extraction_result["account_name"]
                description = extraction_result["description"]
                download_urls = extraction_result["download_urls"]

                if status == STATUS_DEADLINK:
                    insert_record(url, None, None, STATUS_DEADLINK)
                    record_failure(url)

                elif status == STATUS_SUCCESS:
                    download_ok = download_files(download_urls, account_name)
                    if download_ok:
                        insert_record(url, account_name, description, STATUS_SUCCESS)
                    else:
                        insert_record(url, account_name, description, STATUS_FAILED)
                        record_failure(url)

                else:
                    insert_record(url, account_name, description, STATUS_FAILED)
                    record_failure(url)

                time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        finally:
            context.close()

if __name__ == "__main__":
    run()