#!/usr/bin/env python3
"""
Facebook Login - Simple Test Script
Tests the login functionality step-by-step
"""
import logging
import getpass
from src.facebook_crawler import FacebookSeleniumCrawler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_login():
    """
    Test Facebook login functionality
    """
    logger.info("=" * 80)
    logger.info("Facebook Login Test")
    logger.info("=" * 80)

    # Get credentials
    print("\n" + "=" * 80)
    print("ENTER YOUR FACEBOOK CREDENTIALS")
    print("=" * 80)
    
    email = input("\n📧 Enter your Facebook Email/Username: ").strip()
    
    if not email:
        logger.error("Email cannot be empty!")
        return False

    password = getpass.getpass("🔑 Enter your Facebook Password: ")
    
    if not password:
        logger.error("Password cannot be empty!")
        return False

    # Initialize crawler
    crawler = FacebookSeleniumCrawler()

    try:
        logger.info("\n[1] Initializing browser...")
        logger.info("✓ Browser initialized")

        logger.info("\n[2] Attempting login...")
        logger.info(f"   Email: {email}")
        logger.info("   Password: [HIDDEN]")
        
        success = crawler.login(email, password, wait_time=5)

        if success:
            logger.info("\n" + "=" * 80)
            logger.info("✅ LOGIN SUCCESSFUL!")
            logger.info("=" * 80)
            logger.info("\nYou are now authenticated.")
            logger.info("The browser will stay open for 10 seconds...")
            
            import time
            time.sleep(10)
            
            return True
        else:
            logger.error("\n" + "=" * 80)
            logger.error("❌ LOGIN FAILED!")
            logger.error("=" * 80)
            logger.error("\nPossible reasons:")
            logger.error("  - Incorrect email or password")
            logger.error("  - Account is locked or restricted")
            logger.error("  - Two-factor authentication is enabled")
            logger.error("  - Facebook changed the HTML structure")
            logger.error("  - Network issue")
            
            return False

    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        return False

    finally:
        logger.info("\n[3] Closing browser...")
        crawler.close()
        logger.info("✓ Browser closed")


if __name__ == "__main__":
    try:
        success = test_login()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nTest interrupted by user")
        exit(1)
