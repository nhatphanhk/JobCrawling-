"""
Facebook Post Crawler - Project Index
======================================

This is your complete Python project for crawling Facebook posts
and extracting data to CSV files.

# GETTING STARTED:

1. Read the documentation:

   - QUICKSTART.md - Quick start guide (START HERE!)
   - README.md - Full documentation
   - PROJECT_SUMMARY.py - Project overview

2. Install dependencies:
   pip install -r requirements.txt

3. Run examples:
   python main.py # Basic example
   python example_advanced.py # Advanced example

4. Run tests:
   python -m unittest test_crawler.py -v

# PROJECT STRUCTURE:

src/
├── config.py - Configuration (customize here!)
├── facebook_crawler.py - Main crawler class
├── csv_exporter.py - CSV export functionality
└── utils.py - Utility functions

data/ - Input data directory (empty)
output/ - Output CSV files (created automatically)

# FILES:

Core Application:
main.py - Main example script
example_advanced.py - Advanced usage example
test_crawler.py - Unit tests

Documentation:
README.md - Full documentation
QUICKSTART.md - Quick start guide  
 PROJECT_SUMMARY.py - Project overview
.env.example - Configuration template

Configuration:
requirements.txt - Python dependencies
setup.py - Package setup
.gitignore - Git ignore rules

# QUICK COMMANDS:

Install dependencies:
pip install -r requirements.txt

Run main example:
python main.py

Run advanced example:
python example_advanced.py

Run tests:
python -m unittest test_crawler.py -v

Show project overview:
python PROJECT_SUMMARY.py

# FEATURES:

✅ Keyword-based post filtering
✅ Highlight text extraction
✅ CSV export functionality
✅ Engagement statistics
✅ Post sorting and filtering
✅ Comprehensive logging
✅ Retry mechanisms
✅ Unit tests included
✅ Example scripts
✅ Full documentation

# KEY CLASSES:

FacebookCrawler

- Main crawler class
- search_posts(), add_post(), extract_highlighted_text()
- get_posts(), clear_posts()

CSVExporter

- CSV export functionality
- export_posts(), export_posts_by_keyword()
- append_to_csv()

Utility Functions

- filter_posts_by_keywords()
- sort_posts_by_engagement()
- get_post_statistics()
- clean_text(), extract_urls(), extract_hashtags()

# CONFIGURATION:

Edit src/config.py to customize:

SEARCH_KEYWORDS = ["job", "hiring", "recruitment", ...]
OUTPUT_DIR = "./output"
CSV_COLUMNS = ["post_id", "author", "timestamp", ...]
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3

# NEXT STEPS:

1. Read QUICKSTART.md for detailed setup
2. Run python main.py to see it in action
3. Customize src/config.py for your needs
4. Integrate with Facebook Graph API
5. Run unit tests: python -m unittest test_crawler.py -v
6. Check example_advanced.py for advanced patterns

# OUTPUT:

CSV files are saved to output/ directory with:

- post_id, author, timestamp
- content, highlighted_text
- likes, comments, shares
- url

Example filename: facebook_posts_20251209_101530.csv

# NEED HELP?

- Read README.md for comprehensive documentation
- Check QUICKSTART.md for step-by-step setup
- Run python PROJECT_SUMMARY.py for project details
- Review test_crawler.py for usage examples
- Check example_advanced.py for advanced patterns

Happy crawling! 🚀
"""

if **name** == "**main**":
import sys
print(**doc**)
print("\nTo get started:")
print(" 1. Run: pip install -r requirements.txt")
print(" 2. Read: QUICKSTART.md")
print(" 3. Run: python main.py")
