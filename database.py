import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import config

def get_connection():
    return sqlite3.connect(config.DB_PATH)

def init_db():
    """Initializes the SQLite database schema if not present."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                score INTEGER NOT NULL,
                snippet TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notified INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def is_already_seen(link: str) -> bool:
    """Checks whether a link has already been discovered and recorded."""
    # Normalize link (strip trailing slash and tracking params if needed)
    clean_link = link.split("?")[0].rstrip("/")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM opportunities 
            WHERE link = ? OR link LIKE ?
        """, (link, f"{clean_link}%"))
        return cursor.fetchone() is not None

def record_opportunity(link: str, title: str, source: str, category: str, score: int, snippet: str = "") -> bool:
    """Records a new opportunity. Returns True if inserted, False if duplicate."""
    if is_already_seen(link):
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO opportunities (link, title, source, category, score, snippet, notified)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (link, title, source, category, score, snippet))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def get_recent_opportunities(limit: int = 15) -> List[Dict]:
    """Retrieves recent recorded opportunities."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, link, title, source, category, score, snippet, found_at
            FROM opportunities
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
