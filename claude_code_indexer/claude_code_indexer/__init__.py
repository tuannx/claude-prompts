"""
Claude Code Indexer - Code indexing tool using Ensmallen graph database
"""

__version__ = "1.2.0"
__author__ = "Tuan Nguyen"
__email__ = "tuannguyen@duck.com"

from .indexer import CodeGraphIndexer
from .cli import main

__all__ = ["CodeGraphIndexer", "main"]