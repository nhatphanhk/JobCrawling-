# Project Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    FACEBOOK POST CRAWLER                         │
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Search     │      │   Extract    │      │   Filter     │  │
│  │  Keywords    │ ───> │ Highlighted  │ ───> │   Posts      │  │
│  │  (config.py) │      │    Text      │      │  (utils.py)  │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                                                       │           │
│                                                       ▼           │
│                                        ┌──────────────────────┐  │
│                                        │ Sort by Engagement   │  │
│                                        │ Calculate Stats      │  │
│                                        └──────────────────────┘  │
│                                                       │           │
│                                                       ▼           │
│                                        ┌──────────────────────┐  │
│                                        │  Export to CSV       │  │
│                                        │ (csv_exporter.py)    │  │
│                                        └──────────────────────┘  │
│                                                       │           │
│                                                       ▼           │
│                                        ┌──────────────────────┐  │
│                                        │ CSV File in output/  │  │
│                                        │  folder             │  │
│                                        └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Module Dependencies

```
main.py / example_advanced.py
    │
    ├── facebook_crawler.py (Main class)
    │   └── config.py (Settings)
    │
    ├── csv_exporter.py (Export functionality)
    │   └── config.py (Settings)
    │
    └── utils.py (Helper functions)
        └── config.py (Settings)

test_crawler.py (Tests)
    ├── facebook_crawler.py
    ├── csv_exporter.py
    └── utils.py
```

## Data Flow

```
INPUT DATA
    │
    ▼
┌─────────────────────────────┐
│  Facebook Posts             │
│  (JSON/dict format)         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ FacebookCrawler             │
│ - Add posts                 │
│ - Extract keywords          │
│ - Filter content            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Processing                  │
│ - Normalize data            │
│ - Filter by keywords        │
│ - Sort by engagement        │
│ - Calculate statistics      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ CSVExporter                 │
│ - Format columns            │
│ - Write CSV file            │
│ - Append mode               │
└──────────────┬──────────────┘
               │
               ▼
OUTPUT CSV FILE
    │
    └── posts_TIMESTAMP.csv
```

## Configuration Hierarchy

```
┌────────────────────────────────┐
│  src/config.py                 │
│  (Default settings)            │
└────────────────────┬───────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    Keywords    Columns      Output Dir
    Timeout     Encoding     Paths
    Retries     Delimiter    Headers
```

## Class Hierarchy

```
FacebookCrawler
├── __init__(keywords)
├── search_posts(query, limit) → List[Dict]
├── extract_highlighted_text(content) → List[str]
├── add_post(post_data) → None
├── get_posts() → List[Dict]
├── clear_posts() → None
├── close() → None
├── __enter__() / __exit__()  (Context manager)
└── (Retry logic for robustness)

CSVExporter
├── __init__(output_dir)
├── export_posts(posts, filename) → Path
├── export_posts_by_keyword(posts) → Dict[str, Path]
├── append_to_csv(posts, filepath) → None
└── get_output_dir() → Path

Utilities
├── clean_text(text) → str
├── extract_urls(text) → List[str]
├── extract_hashtags(text) → List[str]
├── extract_mentions(text) → List[str]
├── normalize_post_data(post) → Dict
├── filter_posts_by_keywords(posts, keywords) → List[Dict]
├── sort_posts_by_engagement(posts) → List[Dict]
└── get_post_statistics(posts) → Dict
```

## File I/O

```
READ:
  - src/config.py (settings)
  - .env (optional environment vars)
  - input CSV (if appending)

WRITE:
  - output/facebook_posts_*.csv (main output)
  - logs/* (logging, if configured)

DIRECTORIES:
  - output/ (auto-created)
  - data/ (user provided, optional)
  - logs/ (user created, optional)
```

## Execution Flow - main.py

```
START
  │
  ├─ Initialize FacebookCrawler with keywords
  │
  ├─ Create sample posts (demo data)
  │
  ├─ Normalize each post with normalize_post_data()
  │
  ├─ Add posts to crawler.posts list
  │
  ├─ Filter posts by keywords
  │    └─ filter_posts_by_keywords()
  │
  ├─ Sort by engagement
  │    └─ sort_posts_by_engagement()
  │
  ├─ Calculate statistics
  │    └─ get_post_statistics()
  │
  ├─ Create CSVExporter
  │
  ├─ Export to CSV
  │    └─ exporter.export_posts()
  │
  ├─ Print results
  │
  ├─ Close crawler
  │
END
```

## Testing Coverage

```
test_crawler.py
├── TestFacebookCrawler
│   ├── test_add_post()
│   ├── test_extract_highlighted_text()
│   └── test_clear_posts()
│
└── TestUtils
    ├── test_clean_text()
    ├── test_extract_urls()
    ├── test_extract_hashtags()
    ├── test_filter_posts_by_keywords()
    ├── test_sort_posts_by_engagement()
    └── test_get_post_statistics()
```

## Configuration Points

```
✏️ CUSTOMIZABLE SETTINGS:

1. Keywords (SEARCH_KEYWORDS)
   └─ What to search for in posts

2. CSV Columns (CSV_COLUMNS)
   └─ What data to export

3. Output Directory (OUTPUT_DIR)
   └─ Where to save CSV files

4. Timeouts & Retries (REQUEST_TIMEOUT, RETRY_ATTEMPTS)
   └─ Network behavior

5. CSV Format (CSV_DELIMITER, CSV_ENCODING)
   └─ File format options

6. Logging (basicConfig)
   └─ Debug and monitoring
```

## Deployment Architecture

```
Development
    │
    ├─ main.py (local testing)
    ├─ example_advanced.py (examples)
    └─ test_crawler.py (unit tests)

    │
    ▼

Production
    │
    ├─ API Integration (Facebook Graph API)
    ├─ Database Storage (PostgreSQL/MongoDB)
    ├─ Scheduled Tasks (APScheduler)
    ├─ Web Dashboard (Flask/Django)
    └─ Email Notifications (SMTP)
```

## Error Handling Strategy

```
Request Error
    │
    ├─ Retry with exponential backoff
    │   (wait = delay × 2^attempt)
    │
    ├─ Log warning message
    │
    ├─ Max retries reached?
    │   ├─ YES → Raise exception
    │   └─ NO → Try again
    │
    └─ Caller handles exception
```

## Performance Characteristics

```
Small Dataset (< 100 posts)
  └─ Memory: < 1MB
  └─ Time: < 1 second
  └─ CSV Size: < 100KB

Medium Dataset (100-1000 posts)
  └─ Memory: 1-10MB
  └─ Time: 1-10 seconds
  └─ CSV Size: 100KB-1MB

Large Dataset (> 1000 posts)
  └─ Consider batch processing
  └─ Database storage recommended
  └─ CSV might be > 1MB
```

---

See README.md for implementation details and CONFIGURATION.md for customization options.
