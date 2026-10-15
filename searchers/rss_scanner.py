import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from typing import List
import config
from filters import evaluate_legitimacy
from .base import Opportunity

class RSSScanner:
    """Scans public job boards and bounty feeds via standard RSS/Atom"""

    def __init__(self):
        self.headers = {"User-Agent": config.DEFAULT_USER_AGENT}

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
        for src in config.RSS_SOURCES:
            name = src["name"]
            url = src["url"]
            category = src["category"]

            try:
                resp = requests.get(url, headers=self.headers, timeout=12)
                if resp.status_code != 200:
                    continue

                root = ET.fromstring(resp.content)

                # 1. Standard RSS 2.0 (<channel><item>...)
                items = root.findall(".//item")
                if items:
                    for item in items[:15]:
                        title = item.findtext("title") or ""
                        link = item.findtext("link") or ""
                        desc = self._clean_html(item.findtext("description") or "")

                        if not title or not link:
                            continue

                        score, is_legit, flags = evaluate_legitimacy(title, desc, link)
                        if is_legit:
                            snippet = desc[:200] + ("..." if len(desc) > 200 else "")
                            opportunities.append(
                                Opportunity(
                                    title=title.strip(),
                                    link=link.strip(),
                                    source=name,
                                    category=category,
                                    score=score,
                                    snippet=snippet,
                                    flags=flags,
                                )
                            )
                    continue

                # 2. Atom Feed (<entry>...)
                entries = root.findall(".//{http://www.w3.org/2005/Atom}entry") or root.findall(".//entry")
                for entry in entries[:15]:
                    title_elem = entry.find("{http://www.w3.org/2005/Atom}title") or entry.find("title")
                    title = title_elem.text if title_elem is not None else ""

                    link_elem = entry.find("{http://www.w3.org/2005/Atom}link") or entry.find("link")
                    link = link_elem.get("href") if link_elem is not None else ""

                    summary_elem = entry.find("{http://www.w3.org/2005/Atom}summary") or entry.find("summary")
                    desc = self._clean_html(summary_elem.text if summary_elem is not None else "")

                    if not title or not link:
                        continue

                    score, is_legit, flags = evaluate_legitimacy(title, desc, link)
                    if is_legit:
                        snippet = desc[:200] + ("..." if len(desc) > 200 else "")
                        opportunities.append(
                            Opportunity(
                                title=title.strip(),
                                link=link.strip(),
                                source=name,
                                category=category,
                                score=score,
                                snippet=snippet,
                                flags=flags,
                            )
                        )

            except Exception:
                continue

        return opportunities
