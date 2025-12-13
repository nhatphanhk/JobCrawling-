"""
Test script for Selenium-based Facebook crawler
"""
import unittest
from src.facebook_crawler import FacebookSeleniumCrawler
from src.utils import extract_highlighted_text


class TestSeleniumCrawler(unittest.TestCase):
    """Test cases for FacebookSeleniumCrawler"""

    def setUp(self):
        """Set up test fixtures"""
        self.crawler = FacebookSeleniumCrawler(keywords=["job", "hiring"])

    def test_crawler_initialization(self):
        """Test crawler initialization"""
        self.assertIsNotNone(self.crawler)
        self.assertEqual(len(self.crawler.keywords), 2)
        self.assertEqual(self.crawler.posts, [])

    def test_extract_highlighted_text(self):
        """Test highlighted text extraction"""
        content = "We are hiring developers for a new job position"
        results = self.crawler.extract_highlighted_text(content)
        self.assertGreater(len(results), 0)
        self.assertIn("job", results)

    def test_extract_highlighted_text_no_match(self):
        """Test when no keywords match"""
        content = "This is random content with no relevant keywords"
        results = self.crawler.extract_highlighted_text(content)
        self.assertEqual(len(results), 0)

    def test_get_posts_empty(self):
        """Test getting posts when none collected"""
        posts = self.crawler.get_posts()
        self.assertEqual(len(posts), 0)

    def test_clear_posts(self):
        """Test clearing posts"""
        # Add dummy post
        self.crawler.posts.append({"post_id": "test"})
        self.assertGreater(len(self.crawler.posts), 0)

        # Clear
        self.crawler.clear_posts()
        self.assertEqual(len(self.crawler.posts), 0)

    def test_context_manager(self):
        """Test context manager functionality"""
        with FacebookSeleniumCrawler(keywords=["job"]) as crawler:
            self.assertIsNotNone(crawler)
            self.assertIsNone(crawler.driver)  # Driver not created until open_facebook_page

    def test_post_data_structure(self):
        """Test post data structure"""
        crawler = FacebookSeleniumCrawler(keywords=["test"])

        # Create dummy post
        dummy_post = {
            "post_id": "001",
            "author": "Test Author",
            "timestamp": "2025-12-09",
            "content": "Test content",
            "highlighted_text": "test",
            "likes": 10,
            "comments": 5,
            "shares": 2,
            "url": "https://facebook.com/test"
        }

        crawler.posts.append(dummy_post)
        posts = crawler.get_posts()

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["post_id"], "001")
        self.assertEqual(posts[0]["author"], "Test Author")
        self.assertEqual(posts[0]["likes"], 10)

    def test_seen_posts_tracking(self):
        """Test duplicate post detection"""
        crawler = FacebookSeleniumCrawler(keywords=["job"])

        # Add post to seen
        crawler.seen_posts.add("post_001")
        self.assertIn("post_001", crawler.seen_posts)

        # Add another
        crawler.seen_posts.add("post_002")
        self.assertEqual(len(crawler.seen_posts), 2)

    def test_extract_metric_helper(self):
        """Test metric extraction helper"""
        from bs4 import BeautifulSoup

        # Create sample HTML
        html = '<div><span>45 likes</span><span>12 comments</span></div>'
        soup = BeautifulSoup(html, "html.parser")

        crawler = FacebookSeleniumCrawler()
        metric = crawler._extract_metric(soup, "likes")
        self.assertEqual(metric, 45)

    def test_keywords_case_insensitive(self):
        """Test that keyword matching is case-insensitive"""
        crawler = FacebookSeleniumCrawler(keywords=["Job", "HIRING"])

        content = "We are hiring developers for this job opportunity"
        results = crawler.extract_highlighted_text(content)

        self.assertGreater(len(results), 0)

    def test_driver_setup(self):
        """Test Chrome driver setup (without opening page)"""
        try:
            crawler = FacebookSeleniumCrawler()
            driver = crawler.setup_driver()
            self.assertIsNotNone(driver)
            driver.quit()
        except Exception as e:
            # Skip if Chrome not installed
            self.skipTest(f"Chrome not available: {e}")

    def tearDown(self):
        """Clean up after tests"""
        if self.crawler.driver:
            self.crawler.close()


class TestSeleniumIntegration(unittest.TestCase):
    """Integration tests (slower, test actual functionality)"""

    def test_crawler_lifecycle(self):
        """Test complete crawler lifecycle"""
        crawler = FacebookSeleniumCrawler(keywords=["test"])

        # Initialize
        self.assertIsNotNone(crawler)
        self.assertEqual(len(crawler.posts), 0)

        # Add posts
        test_post = {
            "post_id": "test_001",
            "author": "Test",
            "timestamp": "2025-12-09",
            "content": "Testing the crawler",
            "highlighted_text": "test",
            "likes": 5,
            "comments": 2,
            "shares": 1,
            "url": "https://test.com"
        }

        crawler.posts.append(test_post)
        self.assertEqual(len(crawler.get_posts()), 1)

        # Clear
        crawler.clear_posts()
        self.assertEqual(len(crawler.get_posts()), 0)

        # Cleanup
        crawler.close()


if __name__ == "__main__":
    unittest.main()
