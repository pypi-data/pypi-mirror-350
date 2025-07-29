"""Job Posting Parser - Extract structured data from job postings using OpenAI"""

__version__ = "0.2.0"

from .config import config
from .models import JobPosting
from .parser import JobPostingParser

__all__ = ["JobPostingParser", "JobPosting", "config"]
