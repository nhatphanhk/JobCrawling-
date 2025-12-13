"""
Configuration settings for Facebook crawler
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Facebook crawl settings
FACEBOOK_BASE_URL = "https://www.facebook.com"
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

# CSV output settings
CSV_DELIMITER = ","
CSV_ENCODING = "utf-8-sig"  # UTF-8 with BOM for Excel compatibility

# Headers for requests
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Highlight text patterns to search
# These can be keywords or phrases to filter posts
SEARCH_KEYWORDS = [
    "job",
    "hiring",
    "recruitment",
    "vacancy",
    "position",
]

# CSV column names
CSV_COLUMNS = [
    "post_id",
    "author",
    "timestamp",
    "content",
    "highlighted_text",
    "likes",
    "comments",
    "shares",
    "url"
]

# Selenium Settings
SELENIUM_HEADLESS = False  # Set to True for headless mode
SELENIUM_TIMEOUT = 10  # Page load timeout
SELENIUM_IMPLICIT_WAIT = 5  # Implicit wait time
MAX_SCROLLS = 10  # Maximum number of scrolls
SCROLL_PAUSE_TIME = 3  # Seconds to wait after each scroll for content to load
SCROLL_DISTANCE = 500  # Pixels to scroll each time

# Browser settings
BROWSER_WINDOW_WIDTH = 1920
BROWSER_WINDOW_HEIGHT = 1080

# Disable images for faster loading (optional)
DISABLE_IMAGES = True
