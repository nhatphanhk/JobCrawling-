# Facebook Job Crawler 🔍

A Python automation tool for crawling job postings from Facebook. This project helps you collect and analyze job opportunities posted on Facebook's job search platform.

## Features ✨

- 🤖 Automated job scraping from Facebook
- 📊 Export data in multiple formats (CSV, JSON, Excel)
- 🔧 Configurable search parameters (keywords, location, etc.)
- 🎯 Customizable data extraction
- 📝 Detailed logging
- 🚀 Easy to use command-line interface

## Requirements 📋

- Python 3.8 or higher
- Chrome/Chromium browser
- Internet connection

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/nhatphanhk/JobCrawling-.git
cd JobCrawling-
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file for Facebook credentials:
```bash
cp .env.example .env
# Edit .env with your credentials if needed
```

## Usage 💻

### Basic Usage

Run the crawler with default settings:
```bash
python main.py
```

### Advanced Usage

#### Search with specific keywords:
```bash
python main.py --keywords "software engineer"
```

#### Specify location:
```bash
python main.py --keywords "data scientist" --location "San Francisco"
```

#### Control number of jobs to scrape:
```bash
python main.py --max-jobs 100
```

#### Choose output format:
```bash
# Save as JSON
python main.py --output-format json

# Save as Excel
python main.py --output-format excel

# Save as CSV (default)
python main.py --output-format csv
```

#### Run with visible browser (disable headless mode):
```bash
python main.py --no-headless
```

#### Combine multiple options:
```bash
python main.py --keywords "python developer" --location "Vietnam" --max-jobs 50 --output-format json --no-headless
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--keywords` | Job keywords to search for | None |
| `--location` | Location to search in | Vietnam |
| `--max-jobs` | Maximum number of jobs to scrape | 50 |
| `--output-format` | Output format (csv, json, excel) | csv |
| `--output-file` | Output filename (without extension) | facebook_jobs |
| `--no-headless` | Run browser in visible mode | False (headless) |

## Configuration ⚙️

Edit `config.py` to customize default settings:

- `DEFAULT_LOCATION`: Default search location
- `MAX_JOBS_TO_SCRAPE`: Default maximum jobs to scrape
- `OUTPUT_DIR`: Directory for output files
- `OUTPUT_FORMAT`: Default output format
- `HEADLESS_MODE`: Run browser in headless mode
- And more...

## Output 📁

Scraped data is saved in the `data/` directory with the following information for each job:

- Job Title
- Company Name
- Location
- Job Type (if available)
- Description (if available)
- URL
- Posted Date (if available)
- Salary (if available)
- Requirements (if available)
- Scraped Timestamp

## Project Structure 📂

```
JobCrawling-/
├── src/
│   ├── __init__.py
│   ├── crawlers/
│   │   ├── __init__.py
│   │   └── facebook_crawler.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── job_model.py
│   └── utils/
│       ├── __init__.py
│       ├── data_saver.py
│       └── logger.py
├── data/                    # Output directory
├── config.py               # Configuration file
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment file
└── README.md              # This file
```

## Important Notes ⚠️

1. **Facebook's Terms of Service**: Please review Facebook's Terms of Service and robots.txt before scraping. Use this tool responsibly and ethically.

2. **Rate Limiting**: Facebook may implement rate limiting or anti-bot measures. The crawler includes delays and respectful crawling practices.

3. **Page Structure Changes**: Facebook frequently updates its page structure. The crawler may need updates to adapt to these changes.

4. **Login Requirements**: Some job listings may require Facebook login. You can optionally provide credentials in the `.env` file.

5. **Legal Considerations**: Ensure your use of this tool complies with local laws and Facebook's policies regarding data collection.

## Troubleshooting 🔧

### No jobs scraped
- Facebook's page structure may have changed
- Try running with `--no-headless` to see what's happening
- Check if Facebook requires login for job viewing
- Verify your internet connection

### Chrome driver issues
- The tool uses `webdriver-manager` to automatically download the correct driver
- Ensure Chrome/Chromium is installed on your system
- Try updating the `selenium` package

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.8 or higher

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer ⚖️

This tool is for educational and research purposes only. Users are responsible for ensuring their use complies with Facebook's Terms of Service and all applicable laws. The authors are not responsible for any misuse of this tool.

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.
