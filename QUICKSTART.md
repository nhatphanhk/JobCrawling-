# Quick Start Guide

## Installation

1. **Navigate to the project directory:**

```bash
cd d:\Project\Python\JobCrawling-
```

2. **Create a virtual environment (recommended):**

```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Running the Crawler

### Option 1: Run the example script

```bash
python main.py
```

This will:

- Create sample posts with job-related content
- Filter posts by keywords
- Sort by engagement metrics
- Export to CSV file in `output/` directory

**Output:**

```
================================================================================
FACEBOOK POST CRAWLER - RESULTS
================================================================================

Total Posts Collected: 3
Posts with Keywords: 3

Statistics:
  total_posts: 3
  total_likes: 146
  total_comments: 43
  total_shares: 28
  avg_likes: 48.67
  avg_comments: 14.33
  avg_shares: 9.33

CSV Export Location: output/facebook_posts_20251209_HHMMSS.csv

Top Posts by Engagement:
1. Tech Recruitment
   Content: Exciting job opportunity: Full-time position available...
   Engagement: 105 (Likes: 67, Comments: 23, Shares: 15)
================================================================================
```

### Option 2: Run the advanced example

```bash
python example_advanced.py
```

This demonstrates:

- Custom keyword filtering
- Advanced post sorting
- Employment-focused crawling

### Option 3: Run tests

```bash
python -m pytest test_crawler.py -v
```

Or with unittest:

```bash
python -m unittest test_crawler.py -v
```

## Project Structure

```
JobCrawling-/
├── src/
│   ├── config.py              # Configuration settings
│   ├── facebook_crawler.py     # Main crawler class
│   ├── csv_exporter.py         # CSV export functionality
│   └── utils.py                # Utility functions
├── output/                     # Output CSV files
├── main.py                     # Example usage
├── example_advanced.py         # Advanced example
├── test_crawler.py             # Unit tests
└── requirements.txt            # Dependencies
```

## Basic Usage in Your Code

```python
from src.facebook_crawler import FacebookCrawler
from src.csv_exporter import CSVExporter

# Create crawler
crawler = FacebookCrawler(keywords=["job", "hiring"])

# Add posts
post = {
    "post_id": "001",
    "author": "Company",
    "timestamp": "2025-12-09 10:00:00",
    "content": "We are hiring developers",
    "highlighted_text": "hiring",
    "likes": 50,
    "comments": 20,
    "shares": 10,
    "url": "https://facebook.com/post/001"
}
crawler.add_post(post)

# Export to CSV
exporter = CSVExporter()
csv_path = exporter.export_posts(crawler.get_posts())
print(f"Saved to: {csv_path}")
```

## Configuration

Edit `src/config.py` to customize:

```python
# Keywords to search for
SEARCH_KEYWORDS = ["job", "hiring", "recruitment"]

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "output"

# CSV columns
CSV_COLUMNS = ["post_id", "author", "timestamp", "content", ...]

# Request settings
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
```

## Features

✅ Keyword-based post filtering  
✅ Highlight text extraction  
✅ CSV export with multiple options  
✅ Engagement statistics  
✅ Post sorting and filtering  
✅ Comprehensive logging  
✅ Retry mechanisms  
✅ Unit tests included

## Output Files

CSV files are saved to `output/` directory with format:

- `facebook_posts_YYYYMMDD_HHMMSS.csv`

Each row contains:

- Post ID, Author, Timestamp
- Full content and highlighted text
- Engagement metrics (likes, comments, shares)
- Original post URL

## Next Steps

1. **Integrate with Facebook Graph API** for real data:

   - Get access token from Facebook Developer Portal
   - Implement API request in `facebook_crawler.py`

2. **Add database support**:

   - Connect to PostgreSQL/MongoDB for larger datasets
   - Implement data persistence

3. **Schedule crawling**:

   - Use `APScheduler` for periodic crawling
   - Set up background workers

4. **Advanced analysis**:
   - Add sentiment analysis with `TextBlob` or `VADER`
   - Implement topic modeling
   - Create visualizations with `matplotlib`

## Troubleshooting

**Module not found error:**

```bash
pip install -r requirements.txt
```

**Permission denied on output directory:**
Ensure `output/` directory exists and is writable

**CSV encoding issues (Excel):**
Uses UTF-8 with BOM by default for Excel compatibility

## Support

For issues and questions, check:

- README.md for detailed documentation
- test_crawler.py for usage examples
- example_advanced.py for advanced patterns

---

Happy crawling! 🚀
