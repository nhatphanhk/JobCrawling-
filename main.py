#!/usr/bin/env python3
"""
Facebook Job Crawler - Main Entry Point

This script crawls job postings from Facebook and saves them to a file.
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crawlers.facebook_crawler import FacebookJobCrawler, create_facebook_job_url
from src.utils.data_saver import DataSaver
from src.utils.logger import setup_logger
import config


def main():
    """Main function to run the crawler"""
    parser = argparse.ArgumentParser(
        description='Crawl job postings from Facebook',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --keywords "software engineer" --location "San Francisco"
  python main.py --max-jobs 100 --output-format json
  python main.py --no-headless
        """
    )
    
    parser.add_argument(
        '--keywords',
        type=str,
        default=None,
        help='Job keywords to search for (e.g., "software engineer")'
    )
    
    parser.add_argument(
        '--location',
        type=str,
        default=config.DEFAULT_LOCATION,
        help=f'Location to search in (default: {config.DEFAULT_LOCATION})'
    )
    
    parser.add_argument(
        '--max-jobs',
        type=int,
        default=config.MAX_JOBS_TO_SCRAPE,
        help=f'Maximum number of jobs to scrape (default: {config.MAX_JOBS_TO_SCRAPE})'
    )
    
    parser.add_argument(
        '--output-format',
        type=str,
        choices=['csv', 'json', 'excel'],
        default=config.OUTPUT_FORMAT,
        help=f'Output file format (default: {config.OUTPUT_FORMAT})'
    )
    
    parser.add_argument(
        '--output-file',
        type=str,
        default=config.OUTPUT_FILENAME,
        help=f'Output filename without extension (default: {config.OUTPUT_FILENAME})'
    )
    
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in visible mode (not headless)'
    )
    
    args = parser.parse_args()
    
    # Setup logger
    logger = setup_logger()
    
    logger.info("=" * 60)
    logger.info("Facebook Job Crawler Starting")
    logger.info("=" * 60)
    logger.info(f"Keywords: {args.keywords or 'None (browsing all jobs)'}")
    logger.info(f"Location: {args.location}")
    logger.info(f"Max jobs: {args.max_jobs}")
    logger.info(f"Output format: {args.output_format}")
    logger.info(f"Headless mode: {not args.no_headless}")
    logger.info("=" * 60)
    
    try:
        # Create search URL
        search_url = create_facebook_job_url(
            keywords=args.keywords,
            location=args.location
        )
        logger.info(f"Search URL: {search_url}")
        
        # Initialize crawler
        crawler = FacebookJobCrawler(
            headless=not args.no_headless,
            implicit_wait=config.IMPLICIT_WAIT
        )
        
        # Crawl jobs
        jobs = crawler.crawl_jobs(search_url, max_jobs=args.max_jobs)
        
        if not jobs:
            logger.warning("No jobs were scraped. This might be due to:")
            logger.warning("1. Facebook's page structure has changed")
            logger.warning("2. No jobs available for the search criteria")
            logger.warning("3. Facebook requires login to view jobs")
            logger.warning("4. Rate limiting or anti-bot measures")
            return
        
        # Save results
        logger.info(f"Saving {len(jobs)} jobs...")
        data_saver = DataSaver(output_dir=config.OUTPUT_DIR)
        jobs_dict = crawler.get_jobs_as_dict()
        data_saver.save(jobs_dict, format=args.output_format, filename=args.output_file)
        
        logger.info("=" * 60)
        logger.info(f"Successfully scraped and saved {len(jobs)} jobs!")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("\nCrawling interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
