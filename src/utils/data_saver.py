"""
Data saving utilities
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import List
from datetime import datetime


class DataSaver:
    """Handles saving job data to various formats"""
    
    def __init__(self, output_dir: str = "data"):
        """
        Initialize DataSaver
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save_to_csv(self, jobs: List[dict], filename: str = None):
        """
        Save jobs to CSV file
        
        Args:
            jobs: List of job dictionaries
            filename: Output filename (without extension)
        """
        if not jobs:
            print("No jobs to save")
            return
        
        if filename is None:
            filename = f"facebook_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.output_dir / f"{filename}.csv"
        
        df = pd.DataFrame(jobs)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Saved {len(jobs)} jobs to {filepath}")
    
    def save_to_json(self, jobs: List[dict], filename: str = None):
        """
        Save jobs to JSON file
        
        Args:
            jobs: List of job dictionaries
            filename: Output filename (without extension)
        """
        if not jobs:
            print("No jobs to save")
            return
        
        if filename is None:
            filename = f"facebook_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(jobs)} jobs to {filepath}")
    
    def save_to_excel(self, jobs: List[dict], filename: str = None):
        """
        Save jobs to Excel file
        
        Args:
            jobs: List of job dictionaries
            filename: Output filename (without extension)
        """
        if not jobs:
            print("No jobs to save")
            return
        
        if filename is None:
            filename = f"facebook_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.output_dir / f"{filename}.xlsx"
        
        df = pd.DataFrame(jobs)
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"Saved {len(jobs)} jobs to {filepath}")
    
    def save(self, jobs: List[dict], format: str = "csv", filename: str = None):
        """
        Save jobs in specified format
        
        Args:
            jobs: List of job dictionaries
            format: Output format (csv, json, or excel)
            filename: Output filename (without extension)
        """
        if format.lower() == "csv":
            self.save_to_csv(jobs, filename)
        elif format.lower() == "json":
            self.save_to_json(jobs, filename)
        elif format.lower() == "excel":
            self.save_to_excel(jobs, filename)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'csv', 'json', or 'excel'")
