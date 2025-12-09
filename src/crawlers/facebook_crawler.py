"""
Facebook Job Crawler
"""

import time
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from ..models.job_model import Job
from ..utils.logger import setup_logger


class FacebookJobCrawler:
    """Crawler for Facebook job postings"""
    
    def __init__(self, headless: bool = True, implicit_wait: int = 10):
        """
        Initialize the crawler
        
        Args:
            headless: Run browser in headless mode
            implicit_wait: Implicit wait time in seconds
        """
        self.logger = setup_logger()
        self.headless = headless
        self.implicit_wait = implicit_wait
        self.driver = None
        self.jobs = []
        
    def _setup_driver(self):
        """Setup Selenium WebDriver"""
        self.logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(self.implicit_wait)
            self.logger.info("Chrome WebDriver setup successful")
        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {e}")
            raise
    
    def _scroll_page(self, num_scrolls: int = 3, pause_time: float = 2):
        """
        Scroll page to load more content
        
        Args:
            num_scrolls: Number of times to scroll
            pause_time: Pause time between scrolls
        """
        for i in range(num_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            self.logger.debug(f"Scrolled {i+1}/{num_scrolls}")
    
    def _parse_job_element(self, job_element) -> Optional[Job]:
        """
        Parse a job element and extract information
        
        Args:
            job_element: BeautifulSoup element containing job data
            
        Returns:
            Job object or None if parsing fails
        """
        try:
            # This is a generic parser - actual selectors may need adjustment
            # based on Facebook's current HTML structure
            
            title = job_element.get_text(strip=True) if job_element else "Unknown"
            
            # Create a basic job object
            # Note: Facebook's structure changes frequently, so this is a template
            job = Job(
                title=title[:100] if len(title) > 100 else title,
                company="Unknown",
                location="Unknown",
                url=self.driver.current_url
            )
            
            return job
            
        except Exception as e:
            self.logger.error(f"Error parsing job element: {e}")
            return None
    
    def crawl_jobs(self, search_url: str, max_jobs: int = 50) -> List[Job]:
        """
        Crawl jobs from Facebook
        
        Args:
            search_url: URL to start crawling from
            max_jobs: Maximum number of jobs to scrape
            
        Returns:
            List of Job objects
        """
        self.logger.info(f"Starting to crawl jobs from: {search_url}")
        self.jobs = []
        
        try:
            self._setup_driver()
            self.driver.get(search_url)
            time.sleep(3)  # Wait for page to load
            
            self.logger.info("Page loaded, scrolling to load more content...")
            self._scroll_page(num_scrolls=5, pause_time=2)
            
            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Note: Facebook's job search structure requires specific selectors
            # This is a template that demonstrates the approach
            self.logger.info("Parsing job listings...")
            
            # Example: Find all job-related elements
            # These selectors are placeholders and need to be updated based on 
            # Facebook's actual HTML structure
            job_elements = soup.find_all(['a', 'div'], limit=max_jobs)
            
            self.logger.info(f"Found {len(job_elements)} potential job elements")
            
            for element in job_elements[:max_jobs]:
                job = self._parse_job_element(element)
                if job and job.title != "Unknown":
                    self.jobs.append(job)
                    self.logger.debug(f"Scraped: {job}")
            
            self.logger.info(f"Successfully scraped {len(self.jobs)} jobs")
            
        except Exception as e:
            self.logger.error(f"Error during crawling: {e}")
            
        finally:
            self.close()
        
        return self.jobs
    
    def get_jobs_as_dict(self) -> List[dict]:
        """
        Get scraped jobs as list of dictionaries
        
        Returns:
            List of job dictionaries
        """
        return [job.to_dict() for job in self.jobs]
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.logger.info("Closing browser...")
            self.driver.quit()
            self.driver = None


def create_facebook_job_url(keywords: str = None, location: str = None) -> str:
    """
    Create a Facebook job search URL
    
    Args:
        keywords: Job keywords to search for
        location: Location to search in
        
    Returns:
        Facebook job search URL
    """
    base_url = "https://www.facebook.com/jobs/search"
    
    params = []
    if keywords:
        # Facebook job search uses query parameters
        params.append(f"q={keywords.replace(' ', '%20')}")
    if location:
        params.append(f"location={location.replace(' ', '%20')}")
    
    if params:
        return f"{base_url}?{'&'.join(params)}"
    return base_url
