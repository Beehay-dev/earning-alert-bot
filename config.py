import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Telegram Bot Config
def get_telegram_token() -> str:
    candidates = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_TOKEN", "BOT_TOKEN", "TELEGRAMBOTTOKEN"]
    for k, v in os.environ.items():
        if k.strip().upper() in candidates and v.strip():
            return v.strip()
    return os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

def get_telegram_chat_id() -> str:
    candidates = ["TELEGRAM_CHAT_ID", "CHAT_ID", "TELEGRAM_ID", "TELEGRAMCHATID"]
    for k, v in os.environ.items():
        if k.strip().upper() in candidates and v.strip():
            return v.strip()
    return os.getenv("TELEGRAM_CHAT_ID", "").strip()

TELEGRAM_BOT_TOKEN = get_telegram_token()
TELEGRAM_CHAT_ID = get_telegram_chat_id()

# Monitoring Settings
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
MIN_LEGITIMACY_SCORE = int(os.getenv("MIN_LEGITIMACY_SCORE", "40"))

# Database path
DB_PATH = BASE_DIR / "opportunities.db"

# User-Agent for requests
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 LegitEarningBot/1.0"

# High-trust domains and platforms
TRUSTED_PLATFORMS = [
    "prolific.com",
    "usertesting.com",
    "outlier.ai",
    "dataannotation.tech",
    "oneforma.com",
    "clickworker.com",
    "appen.com",
    "telusinternational.ai",
    "hackerone.com",
    "bugcrowd.com",
    "intigriti.com",
    "github.com",
    "weworkremotely.com",
    "remoteok.com",
    "wellfound.com",
    "upwork.com",
    "freelancer.com",
    "fiverr.com",
    "reddit.com/r/beermoney",
    "reddit.com/r/WorkOnline",
    "reddit.com/r/forhire",
    "reddit.com/r/freelance_forhire",
]

# Definite Scam Indicators (Penalty or instant rejection)
SCAM_KEYWORDS = [
    "pay registration fee",
    "pay fee first",
    "upfront fee",
    "upfront deposit",
    "deposit required",
    "send btc to receive",
    "send eth to receive",
    "cash app flip",
    "cashapp flip",
    "crypto doubler",
    "investment doubling",
    "guaranteed 100% return",
    "guaranteed profit",
    "whatsapp investment",
    "contact admin on whatsapp",
    "contact manager on whatsapp",
    "telegram investment",
    "pay to unlock",
    "pyramid scheme",
    "gift card generator",
    "wire transfer to claim",
    "send money to get",
    "western union fee",
]

# Reddit subreddits to monitor
REDDIT_SOURCES = [
    {"subreddit": "beermoney", "category": "Micro-Tasks & Surveys", "min_score": 10},
    {"subreddit": "WorkOnline", "category": "Remote Work & Gigs", "min_score": 10},
    {"subreddit": "signupsforpay", "category": "FCFS & Signup Bonuses", "min_score": 1},
    {"subreddit": "freebies", "category": "Freebies & Promo Rewards", "min_score": 5},
    {"subreddit": "TelegramAirdrop", "category": "Telegram Bots & Airdrops", "min_score": 2},
    {"subreddit": "airdrop", "category": "Airdrops & Web3 Rewards", "min_score": 3},
    {"subreddit": "forhire", "category": "Freelance Gigs", "min_score": 5},
    {"subreddit": "freelance_forhire", "category": "Freelance Gigs", "min_score": 3},
    {"subreddit": "bugbounty", "category": "Tech & Bug Bounties", "min_score": 5},
    {"subreddit": "sidehustle", "category": "Side Hustles & Gigs", "min_score": 10},
]

# RSS / Public feeds to monitor
RSS_SOURCES = [
    {
        "name": "WeWorkRemotely - All Remote",
        "url": "https://weworkremotely.com/remote-jobs.rss",
        "category": "Remote Jobs & Freelance",
    },
    {
        "name": "RemoteOK - Remote Gigs",
        "url": "https://remoteok.com/remote-jobs.rss",
        "category": "Remote Jobs & Freelance",
    },
    {
        "name": "GitHub Public Security Advisory / Bounties",
        "url": "https://github.blog/feed/",
        "category": "Tech & Bug Bounties",
    },
]

# Curated Web Search queries for DuckDuckGo
SEARCH_QUERIES = [
    {
        "query": "apps that pay you to register free no deposit 2026",
        "category": "FCFS & Signup Bonuses",
    },
    {
        "query": "first come first serve free signup reward bonus 2026",
        "category": "FCFS Registration Promos",
    },
    {
        "query": "telegram mini app earn free crypto rewards 2026",
        "category": "Telegram Earning Bots",
    },
    {
        "query": "telegram airdrop bot free verified 2026",
        "category": "Telegram Earning Bots",
    },
    {
        "query": "free crypto airdrop testnet verified no deposit 2026",
        "category": "Airdrops & Web3 Rewards",
    },
    {
        "query": "prolific user testing dataannotation sign up earning",
        "category": "Micro-Tasks & User Testing",
    },
    {
        "query": "bug bounty program rewards hackerone bugcrowd 2026",
        "category": "Tech & Bug Bounties",
    },
]
