"""
Facebook Post Crawler with highlight text extraction using Selenium and BeautifulSoup
"""
import logging
import requests
from typing import List, Dict, Optional, Set
from datetime import datetime
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .config import (
    DEFAULT_HEADERS,
    REQUEST_TIMEOUT,
    RETRY_ATTEMPTS,
    RETRY_DELAY,
    SEARCH_KEYWORDS,
    SELENIUM_HEADLESS,
    SELENIUM_TIMEOUT,
    SELENIUM_IMPLICIT_WAIT,
    MAX_SCROLLS,
    SCROLL_PAUSE_TIME,
    SCROLL_DISTANCE,
    BROWSER_WINDOW_WIDTH,
    BROWSER_WINDOW_HEIGHT,
    DISABLE_IMAGES
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacebookCrawler:
    """
    Crawls Facebook posts based on highlighted text patterns
    """

    def __init__(self, keywords: Optional[List[str]] = None):
        """
        Initialize the Facebook crawler

        Args:
            keywords: List of keywords to highlight in posts
        """
        self.keywords = keywords or SEARCH_KEYWORDS
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.posts = []

    def search_posts(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Search for Facebook posts containing specific keywords

        Args:
            query: Search query string
            limit: Maximum number of posts to retrieve

        Returns:
            List of post dictionaries
        """
        logger.info(f"Searching for posts with query: {query}")
        posts = []

        try:
            # This is a placeholder for actual Facebook API or scraping logic
            # In production, you would use Facebook Graph API with proper authentication
            posts = self._fetch_posts_with_retry(query, limit)
        except Exception as e:
            logger.error(f"Error searching posts: {e}")

        return posts

    def _fetch_posts_with_retry(self, query: str, limit: int) -> List[Dict]:
        """
        Fetch posts with retry logic

        Args:
            query: Search query
            limit: Post limit

        Returns:
            List of posts
        """
        for attempt in range(RETRY_ATTEMPTS):
            try:
                logger.info(f"Attempt {attempt + 1}/{RETRY_ATTEMPTS} to fetch posts")
                # Placeholder for actual request
                return self._fetch_posts(query, limit)
            except requests.RequestException as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"Request failed, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to fetch posts after {RETRY_ATTEMPTS} attempts")
                    raise

    def _fetch_posts(self, query: str, limit: int) -> List[Dict]:
        """
        Fetch posts from Facebook

        Args:
            query: Search query
            limit: Post limit

        Returns:
            List of posts
        """
        posts = []
        # Note: Direct web scraping of Facebook is restricted by their ToS
        # Consider using Facebook Graph API with proper authentication instead
        logger.warning("Note: Direct web scraping requires Facebook API access")
        return posts

    def extract_highlighted_text(self, post_content: str) -> List[str]:
        """
        Extract highlighted text from post content based on keywords

        Args:
            post_content: Post content string

        Returns:
            List of highlighted text segments
        """
        highlighted_segments = []
        content_lower = post_content.lower()

        for keyword in self.keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in content_lower:
                # Find all occurrences
                start = 0
                while True:
                    pos = content_lower.find(keyword_lower, start)
                    if pos == -1:
                        break
                    # Extract context around keyword (50 chars before and after)
                    context_start = max(0, pos - 50)
                    context_end = min(len(post_content), pos + len(keyword) + 50)
                    context = post_content[context_start:context_end].strip()
                    highlighted_segments.append(context)
                    start = pos + 1

        return highlighted_segments

    def add_post(self, post_data: Dict) -> None:
        """
        Add a post to the collection

        Args:
            post_data: Post data dictionary
        """
        self.posts.append(post_data)
        logger.debug(f"Added post: {post_data.get('post_id', 'unknown')}")

    def clear_posts(self) -> None:
        """Clear all collected posts"""
        self.posts = []
        logger.info("Cleared all posts")

    def get_posts(self) -> List[Dict]:
        """
        Get all collected posts

        Returns:
            List of post dictionaries
        """
        return self.posts

    def close(self) -> None:
        """Close the session"""
        self.session.close()
        logger.info("Session closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class FacebookSeleniumCrawler:
    """
    Facebook crawler using Selenium for page scrolling and BeautifulSoup for parsing.
    Scrolls through Facebook page, collects posts, and extracts highlighted text.
    """

    def __init__(self, keywords: Optional[List[str]] = None):
        """
        Initialize the Selenium-based Facebook crawler

        Args:
            keywords: List of keywords to highlight in posts
        """
        self.keywords = keywords or SEARCH_KEYWORDS
        self.posts = []
        self.driver = None
        self.seen_posts: Set[str] = set()  # Track seen posts to avoid duplicates
        logger.info(f"Initialized Selenium crawler with keywords: {self.keywords}")

    def setup_driver(self) -> webdriver.Chrome:
        """
        Set up and configure Selenium Chrome driver

        Returns:
            Configured Chrome webdriver
        """
        chrome_options = Options()

        # Headless mode
        if SELENIUM_HEADLESS:
            chrome_options.add_argument("--headless")
            logger.info("Chrome running in headless mode")

        # Disable notifications
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # Disable images for faster loading
        if DISABLE_IMAGES:
            prefs["profile.managed_default_content_settings.images"] = 2
            chrome_options.add_experimental_option("prefs", prefs)
            logger.info("Image loading disabled")

        # Set window size
        chrome_options.add_argument(f"--window-size={BROWSER_WINDOW_WIDTH},{BROWSER_WINDOW_HEIGHT}")

        # Other options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(SELENIUM_TIMEOUT)
            driver.implicitly_wait(SELENIUM_IMPLICIT_WAIT)
            logger.info("Chrome driver initialized successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise

    def open_facebook_page(self, facebook_url: str) -> bool:
        """
        Open Facebook page in Selenium browser

        Args:
            facebook_url: URL of Facebook page to crawl

        Returns:
            True if page loaded successfully, False otherwise
        """
        try:
            if not self.driver:
                self.driver = self.setup_driver()

            logger.info(f"Opening Facebook page: {facebook_url}")
            self.driver.get(facebook_url)
            time.sleep(2)  # Wait for page to load
            logger.info("Page loaded successfully")
            return True

        except TimeoutException:
            logger.error("Page load timed out")
            return False
        except Exception as e:
            logger.error(f"Error opening page: {e}")
            return False

    def login(self, email: str, password: str, wait_time: int = 3) -> bool:
        """
        Login to Facebook using provided email and password

        Args:
            email: Facebook email/username
            password: Facebook password
            wait_time: Time to wait for login to complete (in seconds)

        Returns:
            True if login successful, False otherwise
        """
        try:
            if not self.driver:
                self.driver = self.setup_driver()
                self.driver.get("https://www.facebook.com/")
                time.sleep(2)

            logger.info("Attempting to login to Facebook...")

            # Find and fill email field
            try:
                email_input = self.driver.find_element(By.ID, "email")
                email_input.clear()
                email_input.send_keys(email)
                logger.info("Email entered successfully")
                time.sleep(1)
            except NoSuchElementException:
                logger.error("Email input field not found")
                return False

            # Find and fill password field
            try:
                password_input = self.driver.find_element(By.ID, "pass")
                password_input.clear()
                password_input.send_keys(password)
                logger.info("Password entered successfully")
                time.sleep(1)
            except NoSuchElementException:
                logger.error("Password input field not found")
                return False

            # Find and click login button
            try:
                login_button = self.driver.find_element(By.NAME, "login")
                login_button.click()
                logger.info("Login button clicked")
                time.sleep(wait_time)  # Wait for login to process
            except NoSuchElementException:
                logger.error("Login button not found")
                return False

            # Verify login was successful
            try:
                # Wait for page to load after login
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "pagelet_bluebar_header"))
                )
                logger.info("Login successful! User is now authenticated.")
                return True
            except TimeoutException:
                logger.warning("Login verification timed out, but login may have succeeded")
                return True

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def scroll_page(self, max_scrolls: int = MAX_SCROLLS) -> Dict[str, any]:
        """
        Scroll through Facebook page to load content.
        Stops when:
        - No new content loads
        - max_scrolls is reached
        - Highlighted text is found

        Args:
            max_scrolls: Maximum number of times to scroll

        Returns:
            Dictionary with scroll statistics
        """
        if not self.driver:
            logger.error("Driver not initialized")
            return {"success": False, "scrolls": 0}

        logger.info(f"Starting page scrolling (max {max_scrolls} scrolls)...")
        scroll_count = 0
        previous_height = self.driver.execute_script("return document.body.scrollHeight")
        found_highlighted = False

        for scroll in range(max_scrolls):
            try:
                # Scroll down
                self.driver.execute_script(f"window.scrollBy(0, {SCROLL_DISTANCE});")
                logger.debug(f"Scroll {scroll + 1}: Scrolled down {SCROLL_DISTANCE}px")

                # Wait for new content to load
                time.sleep(SCROLL_PAUSE_TIME)
                scroll_count += 1

                # Get current page height
                current_height = self.driver.execute_script("return document.body.scrollHeight")

                # Parse page and check for highlighted text
                self.parse_and_extract_posts()

                # Check if highlighted text found
                if self._check_highlighted_text_found():
                    logger.info("Highlighted text found! Stopping scroll.")
                    found_highlighted = True
                    break

                # Check if no new content loaded
                if current_height == previous_height:
                    logger.info("No new content loaded. Stopping scroll.")
                    break

                previous_height = current_height
                logger.info(f"Scroll {scroll + 1} complete. Posts collected: {len(self.posts)}")

            except Exception as e:
                logger.error(f"Error during scroll {scroll + 1}: {e}")
                break

        stats = {
            "success": True,
            "scrolls": scroll_count,
            "posts_collected": len(self.posts),
            "highlighted_text_found": found_highlighted
        }
        logger.info(f"Scrolling complete: {stats}")
        return stats

    def parse_and_extract_posts(self) -> int:
        """
        Parse current page HTML with BeautifulSoup and extract posts

        Returns:
            Number of new posts added
        """
        try:
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, "html.parser")

            new_posts = 0

            # Find all posts (Facebook post containers)
            posts_elements = soup.find_all("div", {"data-testid": "post"})
            logger.debug(f"Found {len(posts_elements)} post elements")

            for post_element in posts_elements:
                try:
                    post_data = self._extract_post_data(post_element)
                    if post_data:
                        post_id = post_data.get("post_id")
                        if post_id and post_id not in self.seen_posts:
                            self.seen_posts.add(post_id)
                            self.posts.append(post_data)
                            new_posts += 1
                            logger.debug(f"Added new post: {post_id}")
                except Exception as e:
                    logger.debug(f"Error extracting post data: {e}")
                    continue

            return new_posts

        except Exception as e:
            logger.error(f"Error parsing page: {e}")
            return 0

    def _extract_post_data(self, post_element) -> Optional[Dict]:
        """
        Extract data from a single post element

        Args:
            post_element: BeautifulSoup element of a post

        Returns:
            Dictionary with post data or None if extraction fails
        """
        try:
            # Extract author
            author_elem = post_element.find("strong")
            author = author_elem.get_text(strip=True) if author_elem else "Unknown"

            # Extract timestamp
            timestamp_elem = post_element.find("a", {"data-testid": "post_timestring"})
            timestamp = timestamp_elem.get_text(strip=True) if timestamp_elem else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Extract post content
            content_elem = post_element.find("div", {"data-testid": "post_message"})
            content = content_elem.get_text(strip=True) if content_elem else ""

            # If no content found, try alternative selector
            if not content:
                content_elem = post_element.find("div", {"dir": "auto"})
                content = content_elem.get_text(strip=True) if content_elem else ""

            # Extract highlighted text
            highlighted_text = self.extract_highlighted_text(content)

            # Extract engagement metrics
            likes = self._extract_metric(post_element, "likes")
            comments = self._extract_metric(post_element, "comments")
            shares = self._extract_metric(post_element, "shares")

            # Extract URL
            post_url_elem = post_element.find("a", {"data-testid": "post_timestring"})
            post_url = post_url_elem.get("href") if post_url_elem else ""

            # Generate post ID
            post_id = f"post_{len(self.posts)}_{int(time.time())}"

            if content:  # Only add if we have content
                return {
                    "post_id": post_id,
                    "author": author,
                    "timestamp": timestamp,
                    "content": content,
                    "highlighted_text": " | ".join(highlighted_text) if highlighted_text else "",
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "url": post_url
                }

        except Exception as e:
            logger.debug(f"Error extracting post data: {e}")
            return None

    def _extract_metric(self, post_element, metric_type: str) -> int:
        """
        Extract engagement metric (likes, comments, shares)

        Args:
            post_element: BeautifulSoup post element
            metric_type: Type of metric (likes, comments, shares)

        Returns:
            Metric count as integer
        """
        try:
            metric_elem = post_element.find("span", string=lambda x: x and metric_type.lower() in x.lower())
            if metric_elem:
                text = metric_elem.get_text(strip=True)
                # Extract number from text like "45 likes"
                numbers = ''.join(filter(str.isdigit, text))
                return int(numbers) if numbers else 0
        except Exception as e:
            logger.debug(f"Error extracting {metric_type}: {e}")

        return 0

    def extract_highlighted_text(self, content: str) -> List[str]:
        """
        Extract highlighted text from post content based on keywords

        Args:
            content: Post content string

        Returns:
            List of highlighted text segments
        """
        highlighted_segments = []
        content_lower = content.lower()

        for keyword in self.keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in content_lower:
                highlighted_segments.append(keyword)

        return list(set(highlighted_segments))  # Remove duplicates

    def _check_highlighted_text_found(self) -> bool:
        """
        Check if any highlighted text was found in collected posts

        Returns:
            True if highlighted text found in any post
        """
        for post in self.posts:
            if post.get("highlighted_text"):
                return True
        return False

    def get_posts(self) -> List[Dict]:
        """
        Get all collected posts

        Returns:
            List of post dictionaries
        """
        return self.posts

    def clear_posts(self) -> None:
        """Clear all collected posts"""
        self.posts = []
        self.seen_posts = set()
        logger.info("Posts and seen_posts cleared")

    def close(self) -> None:
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Chrome driver closed")
        self.driver = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
