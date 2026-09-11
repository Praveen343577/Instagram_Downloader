import os

# Target Configuration
TARGET_URL = "https://grabgram.io/en"

# DOM Selectors
INPUT_SELECTOR = "#fetch-input"
SUBMIT_SELECTOR = "#fetch-submit"
RESULT_CONTAINER_SELECTOR = "#fetch-result"
ERROR_CONTAINER_SELECTOR = "#fetch-error"
GRID_SELECTOR = '[data-role="result-grid"]'
ACCOUNT_NAME_SELECTOR = ".text-brand-ink.truncate"
DESCRIPTION_SELECTOR = ".mt-2.text-sm.text-neutral-600.line-clamp-3"
DOWNLOAD_LINK_SELECTOR = "a[download]"

# Resolution Extraction Hierarchy (Descending Preference)
RESOLUTION_HIERARCHY = [
    "4K",
    "1440p",
    "1080p",
    "720p",
    "480p",
    "360p",
    "320×320",
    "240×300",
    "240×240",
    "150×150"
]

# Anti-Bot Delay Configuration (Seconds)
DELAY_MIN = 1.0
DELAY_MAX = 2.0

# File Paths (project-relative)
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
LINKS_FILE = os.path.join(DATA_DIR, "links.txt")
FAILED_FILE = os.path.join(DATA_DIR, "failed.txt")
DB_FILE    = os.path.join(DATA_DIR, "tracker.db")

# Output Path (external — outside project directory)
DOWNLOADS_DIR = r"D:\Projects\Project_11\Instagram"

# Status Constants
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_DEADLINK = "DEADLINK"