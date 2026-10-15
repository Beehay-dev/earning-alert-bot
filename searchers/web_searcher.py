import time
from typing import List
import config
from filters import evaluate_legitimacy
from .base import Opportunity

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

class WebSearcher:
    """Performs live web searches across DuckDuckGo without requiring paid API keys"""

    def __init__(self):
        pass

    def scan(self) -> List[Opportunity]:
        return self.search()

    def search(self) -> List[Opportunity]:
        opportunities = []
        if not DDGS:
            return opportunities

        for item in config.SEARCH_QUERIES:
            query = item["query"]
            category = item["category"]

            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=5))

                for res in results:
                    title = res.get("title", "").strip()
                    link = res.get("href", "").strip()
                    snippet = res.get("body", "").strip()

                    if not title or not link:
                        continue

                    score, is_legit, flags = evaluate_legitimacy(title, snippet, link)
                    if is_legit:
                        opportunities.append(
                            Opportunity(
                                title=title,
                                link=link,
                                source="Live Web Search",
                                category=category,
                                score=score,
                                snippet=snippet[:200] + ("..." if len(snippet) > 200 else ""),
                                flags=flags,
                            )
                        )
                # Polite pacing between search queries
                time.sleep(1)

            except Exception as e:
                continue

        return opportunities
