# Configuration Guide

## Quick Configuration

### 1. Customize Search Keywords

Edit `src/config.py`:

```python
SEARCH_KEYWORDS = [
    "job",
    "hiring",
    "recruitment",
    "vacancy",
    "position",
]
```

Change to your desired keywords:

```python
# Example: For tech jobs
SEARCH_KEYWORDS = [
    "python developer",
    "senior engineer",
    "data scientist",
    "machine learning",
    "remote position",
]

# Example: For any job type
SEARCH_KEYWORDS = [
    "recruitment",
    "we are hiring",
    "job opportunity",
    "now hiring",
]
```

### 2. Customize CSV Output Columns

Edit `src/config.py`:

```python
CSV_COLUMNS = [
    "post_id",
    "author",
    "timestamp",
    "content",
    "highlighted_text",
    "likes",
    "comments",
    "shares",
    "url"
]
```

Remove columns you don't need or add custom ones:

```python
CSV_COLUMNS = [
    "post_id",
    "author",
    "content",
    "likes",
    "url"
]
```

### 3. Change Output Directory

Edit `src/config.py`:

```python
from pathlib import Path
OUTPUT_DIR = Path(__file__).parent.parent / "output"
```

Change to custom location:

```python
OUTPUT_DIR = Path("C:/MyData/facebook_posts")
# or
OUTPUT_DIR = Path("/home/user/crawler_output")
```

### 4. Adjust Request Settings

Edit `src/config.py`:

```python
REQUEST_TIMEOUT = 30        # Seconds to wait for response
RETRY_ATTEMPTS = 3          # Number of retry attempts
RETRY_DELAY = 2             # Seconds between retries
```

For slow connections, increase timeout:

```python
REQUEST_TIMEOUT = 60
RETRY_ATTEMPTS = 5
RETRY_DELAY = 5
```

### 5. Change CSV Format

Edit `src/config.py`:

```python
CSV_DELIMITER = ","                 # or ";" for European format
CSV_ENCODING = "utf-8-sig"          # UTF-8 with BOM for Excel
```

For different delimiters:

```python
CSV_DELIMITER = ";"         # Semicolon (European Excel)
CSV_DELIMITER = "\t"        # Tab-separated values
```

## Environment Variables (Optional)

Create a `.env` file:

```bash
# Copy .env.example
cp .env.example .env

# Edit .env with your values
FACEBOOK_ACCESS_TOKEN=your_token_here
SEARCH_KEYWORDS=job,hiring,recruitment
OUTPUT_DIR=./output
LOG_LEVEL=INFO
```

Load in your code:

```python
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
```

## Logging Configuration

Default logging is configured in `src/config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Set log level (in any module):

```python
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # More verbose
# or
logger.setLevel(logging.WARNING)  # Less verbose
```

## Examples

### Example 1: Tech Jobs Focus

Edit `src/config.py`:

```python
SEARCH_KEYWORDS = [
    "python",
    "developer",
    "engineer",
    "tech",
    "software",
    "remote",
]

CSV_COLUMNS = [
    "author",
    "content",
    "highlighted_text",
    "likes",
    "shares",
    "url"
]
```

### Example 2: Minimal Output

```python
CSV_COLUMNS = [
    "author",
    "content",
    "url"
]
```

### Example 3: High-Volume Crawling

```python
REQUEST_TIMEOUT = 60
RETRY_ATTEMPTS = 5
RETRY_DELAY = 3

# Increase limits for your use case
SEARCH_LIMIT = 1000
```

### Example 4: European Format

```python
CSV_DELIMITER = ";"
CSV_ENCODING = "latin1"
```

## Testing Your Configuration

After making changes, test by running:

```bash
python main.py
```

Check the output:

- Look for CSV file in configured `OUTPUT_DIR`
- Verify columns match your `CSV_COLUMNS` setting
- Check keywords are being detected in `highlighted_text`

## Common Issues

### Issue: "Output directory not found"

**Solution**: Ensure `OUTPUT_DIR` path exists or is writable:

```python
OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

### Issue: "CSV has wrong columns"

**Solution**: Check `CSV_COLUMNS` matches your data keys

### Issue: "No highlighted text"

**Solution**: Verify `SEARCH_KEYWORDS` are in post content

### Issue: "Timeout errors"

**Solution**: Increase `REQUEST_TIMEOUT`:

```python
REQUEST_TIMEOUT = 60  # 60 seconds instead of 30
```

## Advanced Configuration

### Custom Headers

Edit `src/config.py`:

```python
DEFAULT_HEADERS = {
    "User-Agent": "Your Custom User Agent",
    "Accept-Language": "en-US,en;q=0.9",
}
```

### Custom Post Normalization

In your code:

```python
from src.utils import normalize_post_data

custom_post = {
    "post_id": "123",
    "author": "John Doe",
    "timestamp": "2025-12-09",
    "content": "Hiring now!",
    "highlighted_text": "hiring",
    "likes": 50,
    "comments": 10,
    "shares": 5,
    "url": "https://facebook.com/123"
}

normalized = normalize_post_data(custom_post)
crawler.add_post(normalized)
```

## Summary

Key configuration points:

1. **Keywords** - What to search for
2. **Columns** - What data to export
3. **Output** - Where to save files
4. **Timeout** - How long to wait
5. **Retries** - Error handling
6. **Format** - CSV delimiter and encoding

Start with defaults, customize as needed!

See `src/config.py` for all available settings.
