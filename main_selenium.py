"""
Facebook Post Crawler with Selenium - Main Script
Scrapes Facebook posts using Selenium for scrolling and BeautifulSoup for parsing
Extracts posts with highlighted text and exports to CSV
Includes optional Facebook login functionality
"""
import logging
import getpass
from pathlib import Path
from src.facebook_crawler import FacebookSeleniumCrawler
from src.csv_exporter import CSVExporter
from src.utils import (
    filter_posts_by_keywords,
    sort_posts_by_engagement,
    get_post_statistics,
    normalize_post_data
)
from src.config import SEARCH_KEYWORDS, OUTPUT_DIR, MAX_SCROLLS, SCROLL_PAUSE_TIME

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the Selenium-based Facebook crawler
    """
    logger.info("=" * 80)
    logger.info("Starting Facebook Post Crawler with Selenium")
    logger.info("=" * 80)

    # Configuration
    facebook_url = "https://www.facebook.com/"  # Change to target URL
    keywords = SEARCH_KEYWORDS

    # Initialize crawler
    crawler = FacebookSeleniumCrawler(keywords=keywords)

    try:
        # Step 0: Optional Login
        login_choice = input("\n🔐 Do you want to login to Facebook first? (y/n): ").strip().lower()
        
        if login_choice == 'y':
            logger.info("\n[STEP 0] Facebook Login")
            email = input("   📧 Enter Facebook Email/Username: ").strip()
            password = getpass.getpass("   🔑 Enter Facebook Password: ")
            
            if email and password:
                logger.info("   Attempting login...")
                if crawler.login(email, password, wait_time=5):
                    logger.info("   ✓ Login successful!")
                    facebook_url = input("\n   🌐 Enter the page URL to crawl (press Enter for home feed): ").strip()
                    if not facebook_url:
                        facebook_url = "https://www.facebook.com/"
                else:
                    logger.error("   ✗ Login failed. Continuing without login...")
            else:
                logger.warning("   Email or password not provided. Skipping login...")

        # Step 1: Open Facebook page
        logger.info("\n[STEP 1] Opening Facebook page...")
        if not crawler.open_facebook_page(facebook_url):
            logger.error("Failed to open Facebook page")
            return

        # Step 2: Scroll and collect posts
        logger.info("\n[STEP 2] Scrolling page and collecting posts...")
        logger.info(f"Configuration: max_scrolls={MAX_SCROLLS}, scroll_pause={SCROLL_PAUSE_TIME}s")
        scroll_stats = crawler.scroll_page(max_scrolls=MAX_SCROLLS)

        if not scroll_stats.get("success"):
            logger.error("Scrolling failed")
            return

        # Step 3: Parse and extract posts
        logger.info("\n[STEP 3] Parsing and extracting posts...")
        posts = crawler.get_posts()
        logger.info(f"Total posts collected: {len(posts)}")

        if not posts:
            logger.warning("No posts found")
            return

        # Step 4: Filter posts with highlighted text
        logger.info("\n[STEP 4] Filtering posts with highlighted text...")
        highlighted_posts = [p for p in posts if p.get("highlighted_text")]
        logger.info(f"Posts with highlighted text: {len(highlighted_posts)}")

        if not highlighted_posts:
            logger.warning("No posts with highlighted text found")
            return

        # Step 5: Sort by engagement
        logger.info("\n[STEP 5] Sorting posts by engagement...")
        sorted_posts = sort_posts_by_engagement(highlighted_posts)

        # Step 6: Calculate statistics
        logger.info("\n[STEP 6] Calculating statistics...")
        stats = get_post_statistics(sorted_posts)

        # Step 7: Export to CSV
        logger.info("\n[STEP 7] Exporting to CSV...")
        exporter = CSVExporter(output_dir=OUTPUT_DIR)
        csv_path = exporter.export_posts(sorted_posts, filename="facebook_posts_selenium")

        if csv_path:
            logger.info(f"✅ CSV exported successfully to: {csv_path}")
        else:
            logger.error("Failed to export CSV")
            return

        # Display results
        logger.info("\n" + "=" * 80)
        logger.info("FACEBOOK POST CRAWLER - RESULTS (SELENIUM)")
        logger.info("=" * 80)

        logger.info(f"\n📊 Crawling Statistics:")
        logger.info(f"   Scrolls performed: {scroll_stats['scrolls']}")
        logger.info(f"   Total posts collected: {len(posts)}")
        logger.info(f"   Posts with highlighted text: {len(highlighted_posts)}")
        logger.info(f"   Highlighted text found: {scroll_stats['highlighted_text_found']}")

        logger.info(f"\n📈 Engagement Statistics:")
        logger.info(f"   Total posts: {stats['total_posts']}")
        logger.info(f"   Total likes: {stats['total_likes']}")
        logger.info(f"   Total comments: {stats['total_comments']}")
        logger.info(f"   Total shares: {stats['total_shares']}")
        logger.info(f"   Avg likes: {stats['avg_likes']}")
        logger.info(f"   Avg comments: {stats['avg_comments']}")
        logger.info(f"   Avg shares: {stats['avg_shares']}")

        logger.info(f"\n💾 CSV File: {csv_path}")

        logger.info(f"\n⭐ Top {min(5, len(sorted_posts))} Posts by Engagement:")
        for i, post in enumerate(sorted_posts[:5], 1):
            engagement = post.get("likes", 0) + post.get("comments", 0) + post.get("shares", 0)
            logger.info(f"\n{i}. Author: {post['author']}")
            logger.info(f"   Content: {post['content'][:60]}...")
            logger.info(f"   Highlighted: {post['highlighted_text']}")
            logger.info(f"   Engagement: {engagement} (👍 {post['likes']} 💬 {post['comments']} 📤 {post['shares']})")

        logger.info("\n" + "=" * 80)
        logger.info("✅ Crawling completed successfully!")
        logger.info("=" * 80)

    except KeyboardInterrupt:
        logger.info("\n⚠️  Crawler interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error during crawling: {e}", exc_info=True)
    finally:
        # Close browser
        logger.info("\nClosing browser...")
        crawler.close()
        logger.info("Done!")


if __name__ == "__main__":
    main()
