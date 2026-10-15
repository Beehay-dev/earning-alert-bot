from dataclasses import dataclass, field
from typing import List

@dataclass
class Opportunity:
    title: str
    link: str
    source: str
    category: str
    score: int = 50
    snippet: str = ""
    flags: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "source": self.source,
            "category": self.category,
            "score": self.score,
            "snippet": self.snippet,
            "flags": self.flags,
        }
