# 🚀 Legit Earning Opportunity Finder & Alert Bot

An automated tool that monitors curated, high-trust sources across the web for **free, legitimate earning opportunities** (micro-tasks, freelance gigs, paid user testing, bug bounties, and verified Web3 rewards) and delivers clickable links and cards directly to your **Telegram** or local console.

---

## ✨ Features

- **Multi-Source Discovery:**
  - **⚡ FCFS (First-Come, First-Served) & Signup Promos:** Monitors `r/signupsforpay`, `r/freebies`, and web search for early bird registration rewards with no upfront deposit.
  - **🤖 Telegram Earning Bots & Web3 Mini-Apps:** Monitors `r/TelegramAirdrop`, `r/airdrop`, and Telegram task bots (automatically filtering out scams that ask for deposits).
  - **Reddit Communities:** Live monitoring of `r/beermoney`, `r/WorkOnline`, `r/forhire`, `r/bugbounty`, and `r/sidehustle`.
  - **Verified Remote Job & Gig Feeds:** WeWorkRemotely RSS, RemoteOK RSS, GitHub Bounties.
  - **Live Web Search Engine:** DuckDuckGo queries targeted at high-trust platforms (Prolific, UserTesting, Outlier, DataAnnotation).
- **🛡️ Built-in Anti-Scam & Legitimacy Scorer:**
  - Distinguishes free legitimate tasks from scams. Penalizes fake schemes ("deposit required", "crypto multiplier", "pay to unlock").
  - Boosts verified FCFS bonuses and verified Telegram task bots.
  - Only alerts you if the score meets your threshold (default: `>= 40/100`).
- **Telegram Instant Alerts:**
  - Formats cards with urgency badges (`⚡ [FCFS - ACT FAST! LIMITED SPOTS]`, `🤖 [TELEGRAM BOT / MINI-APP]`), legitimacy score, and direct clickable links.
- **De-duplication Engine:**
  - Built-in SQLite database (`opportunities.db`) ensures you are never alerted about the same link twice.
- **Two Execution Modes:**
  - **On-Demand:** Run a single search sweep whenever you want fresh links (`python main.py --run-once`).
  - **Background Daemon:** Runs continuously on a timer (e.g. every 30 mins) and pings your phone whenever something new is spotted (`python main.py --daemon`).

---

## 📋 Quick Setup Guide

### Step 1: Create a Telegram Bot (Takes 2 minutes, 100% Free)

1. Open Telegram and search for **[@BotFather](https://t.me/BotFather)**.
2. Send the command:
   ```text
   /newbot
   ```
3. Follow the prompts to name your bot. BotFather will give you an **API Token** (looks like `123456789:ABCDefGhIJKlmNoPQRsTUVwxyZ`).
4. Now search for **[@userinfobot](https://t.me/userinfobot)** on Telegram and press **Start**. It will reply with your numeric **Id** (e.g. `987654321`).
5. Open your newly created bot in Telegram and click **Start** so it has permission to message you.

---

### Step 2: Configure the Bot

You can configure the bot interactively by running:
```powershell
python main.py --setup
```
*Or* manually edit `.env` in this folder:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
CHECK_INTERVAL_MINUTES=30
MIN_LEGITIMACY_SCORE=40
```

---

### Step 3: Test Telegram Connection

Verify your token and receive a test message:
```powershell
python main.py --test-telegram
```

---

### Step 4: Run the App

#### A. Single Search Sweep (Run once and exit)
```powershell
python main.py --run-once
```

#### B. Continuous Background Monitor (Recommended)
Checks on a recurring schedule and notifies you in real time:
```powershell
python main.py --daemon
```

#### C. View Recent Discoveries & History
```powershell
python main.py --status
```

---

## ⚙️ Customization (`config.py`)

You can easily adjust:
- **`MIN_LEGITIMACY_SCORE`**: Raise to `60` or `70` for stricter filtering, or lower to `30` to see more experimental opportunities.
- **`REDDIT_SOURCES`**: Add or remove subreddits.
- **`RSS_SOURCES`**: Add new RSS job feeds.
- **`SEARCH_QUERIES`**: Tailor search terms to your specific skills (e.g. translation, Python development, transcription).
