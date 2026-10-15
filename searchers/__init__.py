# Package marker for searchers
from .base import Opportunity
from .reddit_scanner import RedditScanner
from .rss_scanner import RSSScanner
from .web_searcher import WebSearcher

__all__ = ["Opportunity", "RedditScanner", "RSSScanner", "WebSearcher"]
