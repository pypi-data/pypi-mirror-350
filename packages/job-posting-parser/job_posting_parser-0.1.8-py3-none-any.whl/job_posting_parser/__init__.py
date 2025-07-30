"""Job Posting Parser - Extract structured data from job postings using OpenAI"""

import importlib.metadata

__version__ = importlib.metadata.version("job-posting-parser")

from .config import config
from .models import JobPosting
from .parser import JobPostingParser

__all__ = ["JobPostingParser", "JobPosting", "config"]
