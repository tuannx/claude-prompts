"""
Claude Code Indexer - Code indexing tool using Ensmallen graph database
"""

try:
    from importlib.metadata import version
    __version__ = version("claude-code-indexer")
except:
    __version__ = "unknown"

__author__ = "Tony Nguyen"
__email__ = "tony@startupascent.net"

from .indexer import CodeGraphIndexer
from .cli import main

__all__ = ["CodeGraphIndexer", "main"]