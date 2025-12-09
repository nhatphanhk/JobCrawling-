#!/usr/bin/env python3
"""
Example usage of Facebook Job Crawler

This script demonstrates how to use the crawler programmatically.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crawlers.facebook_crawler import FacebookJobCrawler, create_facebook_job_url
from src.utils.data_saver import DataSaver
from src.models.job_model import Job


def example_basic_crawl():
    """Example: Basic job crawling"""
    print("=" * 60)
    print("Example 1: Basic Job Crawling")
    print("=" * 60)
    
    # Create search URL
    url = create_facebook_job_url(keywords="software engineer", location="Vietnam")
    print(f"Search URL: {url}")
    
    # Initialize crawler
    crawler = FacebookJobCrawler(headless=True)
    
    # Crawl jobs
    jobs = crawler.crawl_jobs(url, max_jobs=20)
    print(f"Scraped {len(jobs)} jobs")
    
    # Save results
    if jobs:
        saver = DataSaver(output_dir="data")
        jobs_dict = crawler.get_jobs_as_dict()
        saver.save_to_csv(jobs_dict, filename="example_jobs")


def example_create_jobs_manually():
    """Example: Creating job objects manually for testing"""
    print("\n" + "=" * 60)
    print("Example 2: Creating and Saving Jobs Manually")
    print("=" * 60)
    
    # Create sample jobs
    jobs = [
        Job(
            title="Senior Python Developer",
            company="Tech Innovators Inc",
            location="Ho Chi Minh City, Vietnam",
            job_type="Full-time",
            description="Looking for experienced Python developers...",
            url="https://facebook.com/jobs/example1",
            salary="$60,000 - $80,000"
        ),
        Job(
            title="Data Analyst",
            company="Data Solutions Ltd",
            location="Hanoi, Vietnam",
            job_type="Full-time",
            description="Analyze and interpret complex data sets...",
            url="https://facebook.com/jobs/example2",
            salary="Competitive"
        ),
        Job(
            title="Frontend Developer",
            company="Web Designs Co",
            location="Da Nang, Vietnam",
            job_type="Contract",
            description="Create beautiful and responsive web interfaces...",
            url="https://facebook.com/jobs/example3"
        )
    ]
    
    # Display jobs
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job}")
    
    # Convert to dictionaries
    jobs_dict = [job.to_dict() for job in jobs]
    
    # Save in different formats
    saver = DataSaver(output_dir="data")
    print("\nSaving jobs to different formats...")
    saver.save_to_csv(jobs_dict, filename="manual_jobs")
    saver.save_to_json(jobs_dict, filename="manual_jobs")
    saver.save_to_excel(jobs_dict, filename="manual_jobs")


def example_url_generation():
    """Example: Generating Facebook job search URLs"""
    print("\n" + "=" * 60)
    print("Example 3: URL Generation")
    print("=" * 60)
    
    # Various search combinations
    searches = [
        ("python developer", "San Francisco"),
        ("data scientist", "New York"),
        ("full stack engineer", "Remote"),
        (None, "Vietnam"),  # Just location
        ("software engineer", None),  # Just keywords
    ]
    
    for keywords, location in searches:
        url = create_facebook_job_url(keywords, location)
        print(f"Keywords: {keywords or 'None':30} | Location: {location or 'None':15} | {url}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Facebook Job Crawler - Example Usage")
    print("=" * 60)
    
    # Run examples
    example_url_generation()
    example_create_jobs_manually()
    
    # Uncomment to test actual crawling (requires Chrome/Chromium)
    # example_basic_crawl()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
