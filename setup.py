"""
Setup script for Facebook Job Crawler
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="facebook-job-crawler",
    version="1.0.0",
    author="nhatphanhk",
    description="A Python automation tool for crawling job postings from Facebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nhatphanhk/JobCrawling-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "facebook-job-crawler=main:main",
        ],
    },
    keywords="facebook jobs crawler scraper automation selenium",
    project_urls={
        "Bug Reports": "https://github.com/nhatphanhk/JobCrawling-/issues",
        "Source": "https://github.com/nhatphanhk/JobCrawling-",
    },
)
