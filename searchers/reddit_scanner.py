import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import time
from typing import List
import config
from filters import evaluate_legitimacy
from .base import Opportunity

class RedditScanner:
    """Scans curated earning subreddits via official Reddit Atom feeds for maximum reliability"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        self.atom_ns = {"atom": "http://www.w3.org/2005/Atom"}

    def _clean_html(self, raw_html: str) -> str:
        if not raw_html:
            return ""
        try:
            soup = BeautifulSoup(raw_html, "html.parser")
            return soup.get_text(separator=" ", strip=True)
        except Exception:
            return raw_html

    def scan(self) -> List[Opportunity]:
        opportunities = []
        for src in config.REDDIT_SOURCES:
            sub = src["subreddit"]
            category = src["category"]

            feed_url = f"https://www.reddit.com/r/{sub}/new.rss"

            try:
                resp = requests.get(feed_url, headers=self.headers, timeout=12)
                if resp.status_code != 200:
                    continue

                root = ET.fromstring(resp.content)
                entries = root.findall(".//atom:entry", self.atom_ns) or root.findall(".//entry")

                for entry in entries[:15]:
                    title_elem = entry.find("atom:title", self.atom_ns) or entry.find("title")
                    title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

                    link_elem = entry.find("atom:link", self.atom_ns) or entry.find("link")
                    link = link_elem.get("href", "").strip() if link_elem is not None else ""

                    content_elem = entry.find("atom:content", self.atom_ns) or entry.find("content")
                    raw_content = content_elem.text if content_elem is not None and content_elem.text else ""
                    clean_text = self._clean_html(raw_content)

                    if not title or not link:
                        continue

                    # Filter out sticky posts or automated rules
                    if "[meta]" in title.lower() or "weekly discussion" in title.lower() or "read first" in title.lower():
                        continue

                    score, is_legit, flags = evaluate_legitimacy(
                        title=title,
                        text=clean_text,
                        url=link,
                        upvotes=5,  # Baseline positive signal for fresh submissions
                    )

                    if is_legit:
                        snippet = clean_text[:220] + ("..." if len(clean_text) > 220 else "")
                        opportunities.append(
                            Opportunity(
                                title=title,
                                link=link,
                                source=f"Reddit r/{sub}",
                                category=category,
                                score=score,
                                snippet=snippet,
                                flags=flags,
                            )
                        )

            except Exception:
                continue

            time.sleep(1)

        return opportunities
