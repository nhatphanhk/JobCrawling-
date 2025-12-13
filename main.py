"""
Main script for Facebook Post Crawler
Example usage of the crawler
"""
import logging
from pathlib import Path
from src.facebook_crawler import FacebookCrawler
from src.csv_exporter import CSVExporter
from src.utils import (
    filter_posts_by_keywords,
    sort_posts_by_engagement,
    get_post_statistics,
    normalize_post_data
)
from src.config import SEARCH_KEYWORDS, OUTPUT_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the Facebook crawler
    """
    logger.info("Starting Facebook Post Crawler")

    # Initialize crawler with custom keywords
    keywords = SEARCH_KEYWORDS
    crawler = FacebookCrawler(keywords=keywords)

    # Example: Add sample posts for demonstration
    # In production, these would come from actual Facebook API/scraping
    sample_posts = [
        {
            "post_id": "001",
            "author": "Job Board",
            "timestamp": "2025-12-09 10:30:00",
            "content": "We are hiring a senior python developer for our team. Join us! #hiring #python",
            "highlighted_text": "hiring",
            "likes": 45,
            "comments": 12,
            "shares": 8,
            "url": "https://facebook.com/post/001"
        },
        {
            "post_id": "002",
            "author": "Tech Recruitment",
            "timestamp": "2025-12-09 11:15:00",
            "content": "Exciting job opportunity: Full-time position available. Position includes benefits.",
            "highlighted_text": "job, position",
            "likes": 67,
            "comments": 23,
            "shares": 15,
            "url": "https://facebook.com/post/002"
        },
        {
            "post_id": "003",
            "author": "Career Hub",
            "timestamp": "2025-12-09 14:45:00",
            "content": "New vacancy: We are looking for experienced recruitment specialists. Vacancy expires soon!",
            "highlighted_text": "vacancy, recruitment",
            "likes": 34,
            "comments": 8,
            "shares": 5,
            "url": "https://facebook.com/post/003"
        }
    ]

    # Normalize and add posts
    for post in sample_posts:
        normalized = normalize_post_data(post)
        crawler.add_post(normalized)

    logger.info(f"Collected {len(crawler.get_posts())} posts")

    # Filter posts by keywords
    filtered_posts = filter_posts_by_keywords(
        crawler.get_posts(),
        ["hiring", "job", "vacancy", "recruitment"]
    )
    logger.info(f"Filtered to {len(filtered_posts)} posts")

    # Sort by engagement
    sorted_posts = sort_posts_by_engagement(filtered_posts)

    # Get statistics
    stats = get_post_statistics(sorted_posts)
    logger.info(f"Post statistics: {stats}")

    # Export to CSV
    exporter = CSVExporter(output_dir=OUTPUT_DIR)
    csv_path = exporter.export_posts(sorted_posts, filename="facebook_posts_export")
    logger.info(f"Posts exported to: {csv_path}")

    # Display results
    print("\n" + "="*80)
    print("FACEBOOK POST CRAWLER - RESULTS")
    print("="*80)
    print(f"\nTotal Posts Collected: {len(crawler.get_posts())}")
    print(f"Posts with Keywords: {len(filtered_posts)}")
    print(f"\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print(f"\nCSV Export Location: {csv_path}")
    print("\nTop Posts by Engagement:")
    for i, post in enumerate(sorted_posts[:3], 1):
        engagement = post.get("likes", 0) + post.get("comments", 0) + post.get("shares", 0)
        print(f"\n{i}. {post['author']}")
        print(f"   Content: {post['content'][:60]}...")
        print(f"   Engagement: {engagement} (Likes: {post['likes']}, Comments: {post['comments']}, Shares: {post['shares']})")

    print("\n" + "="*80)
    crawler.close()
    logger.info("Crawler completed successfully")


if __name__ == "__main__":
    main()
