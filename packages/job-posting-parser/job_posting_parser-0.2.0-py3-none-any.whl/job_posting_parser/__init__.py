"""Job Posting Parser - Extract structured data from job postings using OpenAI"""

__version__ = "0.2.0"

from .parser import JobPostingParser
from .models import JobPosting
from .config import config

__all__ = ["JobPostingParser", "JobPosting", "config"]
