"""
Job data model
"""

from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Job:
    """Represents a job posting from Facebook"""
    
    title: str
    company: str
    location: str
    job_type: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    posted_date: Optional[str] = None
    salary: Optional[str] = None
    requirements: Optional[str] = None
    scraped_at: str = None
    
    def __post_init__(self):
        """Set scraped timestamp if not provided"""
        if self.scraped_at is None:
            self.scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """Convert job to dictionary"""
        return asdict(self)
    
    def __str__(self):
        return f"Job(title='{self.title}', company='{self.company}', location='{self.location}')"
