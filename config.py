"""
Configuration file for Facebook Job Crawler
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Facebook credentials (optional - for better access)
FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL', '')
FACEBOOK_PASSWORD = os.getenv('FACEBOOK_PASSWORD', '')

# Crawler settings
BASE_URL = "https://www.facebook.com/jobs/search"
HEADLESS_MODE = True  # Set to False to see browser while crawling
IMPLICIT_WAIT = 10  # seconds
PAGE_LOAD_TIMEOUT = 30  # seconds

# Search parameters
DEFAULT_LOCATION = "Vietnam"
DEFAULT_KEYWORDS = ["software engineer", "developer", "data scientist"]

# Output settings
OUTPUT_DIR = "data"
OUTPUT_FORMAT = "csv"  # csv, json, or excel
OUTPUT_FILENAME = "facebook_jobs"

# Crawler behavior
MAX_JOBS_TO_SCRAPE = 50
SCROLL_PAUSE_TIME = 2  # seconds between scrolls
MAX_SCROLL_ATTEMPTS = 10

# Browser settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
