"""
Test script for the Facebook crawler
"""
import unittest
from src.facebook_crawler import FacebookCrawler
from src.csv_exporter import CSVExporter
from src.utils import (
    clean_text,
    extract_urls,
    extract_hashtags,
    filter_posts_by_keywords,
    sort_posts_by_engagement,
    get_post_statistics
)


class TestFacebookCrawler(unittest.TestCase):
    """Test cases for FacebookCrawler"""

    def setUp(self):
        """Set up test fixtures"""
        self.crawler = FacebookCrawler(keywords=["job", "hiring"])
        self.test_post = {
            "post_id": "test_001",
            "author": "Test Author",
            "timestamp": "2025-12-09 10:00:00",
            "content": "We are hiring for a job position",
            "highlighted_text": "hiring, job",
            "likes": 10,
            "comments": 5,
            "shares": 2,
            "url": "https://facebook.com/test"
        }

    def test_add_post(self):
        """Test adding posts"""
        self.crawler.add_post(self.test_post)
        self.assertEqual(len(self.crawler.get_posts()), 1)

    def test_extract_highlighted_text(self):
        """Test highlighted text extraction"""
        content = "We are hiring for a job position with great benefits"
        results = self.crawler.extract_highlighted_text(content)
        self.assertGreater(len(results), 0)

    def test_clear_posts(self):
        """Test clearing posts"""
        self.crawler.add_post(self.test_post)
        self.assertGreater(len(self.crawler.get_posts()), 0)
        self.crawler.clear_posts()
        self.assertEqual(len(self.crawler.get_posts()), 0)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""

    def test_clean_text(self):
        """Test text cleaning"""
        text = "  Hello   World  \n\n  "
        cleaned = clean_text(text)
        self.assertEqual(cleaned, "Hello World")

    def test_extract_urls(self):
        """Test URL extraction"""
        text = "Check this https://example.com and https://test.com"
        urls = extract_urls(text)
        self.assertEqual(len(urls), 2)

    def test_extract_hashtags(self):
        """Test hashtag extraction"""
        text = "Great post #hiring #job #recruitment"
        hashtags = extract_hashtags(text)
        self.assertEqual(len(hashtags), 3)
        self.assertIn("hiring", hashtags)

    def test_filter_posts_by_keywords(self):
        """Test post filtering"""
        posts = [
            {"content": "We are hiring developers"},
            {"content": "Check out our blog"},
            {"content": "Job opportunities available"},
        ]
        filtered = filter_posts_by_keywords(posts, ["hiring", "job"])
        self.assertEqual(len(filtered), 2)

    def test_sort_posts_by_engagement(self):
        """Test post sorting"""
        posts = [
            {"likes": 10, "comments": 5, "shares": 2},
            {"likes": 50, "comments": 20, "shares": 10},
            {"likes": 20, "comments": 8, "shares": 3},
        ]
        sorted_posts = sort_posts_by_engagement(posts)
        # Check if sorted in descending order
        self.assertEqual(sorted_posts[0]["likes"], 50)

    def test_get_post_statistics(self):
        """Test statistics calculation"""
        posts = [
            {"likes": 10, "comments": 5, "shares": 2},
            {"likes": 20, "comments": 10, "shares": 4},
        ]
        stats = get_post_statistics(posts)
        self.assertEqual(stats["total_posts"], 2)
        self.assertEqual(stats["total_likes"], 30)
        self.assertEqual(stats["avg_likes"], 15.0)


if __name__ == "__main__":
    unittest.main()
