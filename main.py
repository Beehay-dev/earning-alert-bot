import argparse
import sys
import time
from datetime import datetime

# Ensure proper unicode handling on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import config
import database
from notifier import TelegramNotifier
from searchers import RedditScanner, RSSScanner, WebSearcher, Opportunity

def print_banner():
    banner = """
===========================================================
 🔍  LEGIT EARNING FINDER & TELEGRAM ALERT BOT  🚀
===========================================================
 Monitoring:
  • Reddit (r/beermoney, r/WorkOnline, r/forhire, r/airdrop)
  • Remote Job & Gig Feeds (WeWorkRemotely, RemoteOK, GitHub)
  • Web Search for Free Verified Testing & Bounties
 Anti-Scam Scoring: Active (Threshold: >= {min_score}/100)
===========================================================
""".format(min_score=config.MIN_LEGITIMACY_SCORE)
    print(banner)

def run_sweep(notifier: TelegramNotifier) -> int:
    """Executes a single discovery sweep across all configured sources."""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔎 Starting earning opportunity search sweep...")
    database.init_db()

    scanners = [
        ("Reddit Scanner", RedditScanner()),
        ("RSS/Gig Feeds", RSSScanner()),
        ("Web Searcher", WebSearcher()),
    ]

    new_found = 0

    for name, scanner in scanners:
        print(f" -> Querying {name}...")
        try:
            results = scanner.scan()
            print(f"    Found {len(results)} potential candidates.")
            for opp in results:
                if database.is_already_seen(opp.link):
                    continue

                # Record in database
                recorded = database.record_opportunity(
                    link=opp.link,
                    title=opp.title,
                    source=opp.source,
                    category=opp.category,
                    score=opp.score,
                    snippet=opp.snippet,
                )

                if recorded:
                    new_found += 1
                    print(f"    [NEW MATCH] [{opp.score}/100] {opp.title[:60]}... ({opp.link})")
                    notifier.send_opportunity(opp)
                    # Pause to stay well clear of Telegram rate limits
                    time.sleep(1.5)

        except Exception as e:
            print(f"    [Error] Exception running {name}: {e}")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Sweep complete. Sent {new_found} new alerts.")
    return new_found

def setup_wizard():
    """Interactive wizard to configure Telegram credentials in .env"""
    print("\n--- 🛠️ Telegram Setup Wizard ---")
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot to create a bot and copy the API Token")
    print("3. Open Telegram and search for @userinfobot (or start your new bot and send a message)")
    print("4. Copy your Chat ID numeric ID\n")

    token = input("Enter your Telegram Bot Token: ").strip()
    chat_id = input("Enter your Telegram Chat ID: ").strip()

    if token and chat_id:
        env_content = f"TELEGRAM_BOT_TOKEN={token}\nTELEGRAM_CHAT_ID={chat_id}\nCHECK_INTERVAL_MINUTES=30\nMIN_LEGITIMACY_SCORE=40\n"
        with open(config.BASE_DIR / ".env", "w") as f:
            f.write(env_content)
        print("✅ Configuration saved to .env file! Now testing...")
        test_notifier = TelegramNotifier(bot_token=token, chat_id=chat_id)
        res = test_notifier.test_connection()
        if res.get("ok"):
            bot_name = res.get("result", {}).get("username", "Unknown")
            print(f"✅ Bot connected successfully: @{bot_name}")
            test_notifier.send_message("🎉 <b>Connection Successful!</b>\nYour Legit Earning Alert Bot is ready and working.")
            print("✅ Test message dispatched to your Telegram!")
        else:
            print(f"⚠️ Telegram returned an error: {res.get('error') or res.get('description')}")
    else:
        print("⚠️ Missing fields. Setup aborted.")

def show_status():
    database.init_db()
    recent = database.get_recent_opportunities(limit=10)
    print(f"\n📊 Total recent recorded opportunities: {len(recent)}")
    for item in recent:
        print(f" • [{item['score']}/100] {item['category']} | {item['title'][:50]} | {item['link']}")

def run_web_service(notifier: TelegramNotifier):
    """Starts a lightweight HTTP server on $PORT for Render Free Web Service, with background sweep worker."""
    import os
    import json
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler

    port = int(os.environ.get("PORT", 10000))

    class RenderHealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path in ("/", "/health"):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                data = {
                    "status": "online",
                    "service": "Legit Earning Opportunity Alert Bot",
                    "interval_minutes": config.CHECK_INTERVAL_MINUTES,
                    "timestamp": datetime.now().isoformat(),
                }
                self.wfile.write(json.dumps(data).encode("utf-8"))
            elif self.path == "/sweep":
                active_notifier = TelegramNotifier()
                new_items = run_sweep(active_notifier)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "sweep_complete", "new_matches": new_items}).encode("utf-8"))
            elif self.path == "/test":
                from dotenv import load_dotenv
                load_dotenv(config.BASE_DIR / ".env", override=True)

                current_token = config.get_telegram_token()
                current_chat_id = config.get_telegram_chat_id()
                active_notifier = TelegramNotifier(bot_token=current_token, chat_id=current_chat_id)

                connection = active_notifier.test_connection()
                send_result = active_notifier.send_message_detailed("🔔 <b>Render Test Alert:</b> Your Telegram bot is connected and working successfully!")
                matching_keys = [k for k in os.environ.keys() if any(w in k.upper() for w in ("TELEGRAM", "BOT", "CHAT", "TOKEN"))]

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                diag = {
                    "token_configured": bool(current_token),
                    "token_preview": (current_token[:6] + "..." + current_token[-4:]) if current_token else None,
                    "chat_id_configured": bool(current_chat_id),
                    "chat_id_value": current_chat_id or None,
                    "matching_env_keys_on_server": matching_keys,
                    "telegram_getMe": connection,
                    "send_message_result": send_result,
                }
                self.wfile.write(json.dumps(diag).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            return

    def background_worker():
        import schedule
        print(f"⏱️ Background scanner active. Interval: every {config.CHECK_INTERVAL_MINUTES} minutes.")
        run_sweep(notifier)
        schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(run_sweep, notifier=notifier)
        while True:
            schedule.run_pending()
            time.sleep(1)

    worker_thread = threading.Thread(target=background_worker, daemon=True)
    worker_thread.start()

    server = HTTPServer(("0.0.0.0", port), RenderHealthHandler)
    print(f"🌐 Web health-check server listening on 0.0.0.0:{port} for Render deployment...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopping...")

def main():
    parser = argparse.ArgumentParser(description="Legit Earning Opportunities Search & Alert App")
    parser.add_argument("--run-once", action="store_true", help="Run a single search sweep and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background on a schedule")
    parser.add_argument("--web", action="store_true", help="Run HTTP health-check server for Render cloud deployment")
    parser.add_argument("--test-telegram", action="store_true", help="Test Telegram bot token & send test message")
    parser.add_argument("--status", action="store_true", help="Show recent discovered opportunities")
    parser.add_argument("--setup", action="store_true", help="Run interactive setup wizard for Telegram credentials")

    args = parser.parse_args()
    print_banner()

    if args.setup:
        setup_wizard()
        return

    if args.status:
        show_status()
        return

    notifier = TelegramNotifier()

    if args.test_telegram:
        if not notifier.is_configured:
            print("⚠️ Telegram is not configured yet. Run with --setup or fill in .env file.")
            return
        res = notifier.test_connection()
        if res.get("ok"):
            bot_name = res.get("result", {}).get("username", "Unknown")
            print(f"✅ Bot verification passed! Bot handle: @{bot_name}")
            sent = notifier.send_message("🔔 <b>Test Alert:</b> Your Legit Earning Alert Bot is online and configured properly!")
            if sent:
                print("✅ Test message sent to your Telegram chat!")
        else:
            print(f"❌ Connection failed: {res.get('error') or res.get('description')}")
        return

    if not notifier.is_configured:
        print("⚠️ Note: Telegram credentials not yet set in .env.")
        print("   Alerts will be printed to this console until Telegram is configured.")
        print("   (To set up Telegram, run: python main.py --setup)\n")

    if args.web:
        run_web_service(notifier)
        return

    if args.daemon:
        import schedule
        print(f"⏱️ Running in background daemon mode. Checks every {config.CHECK_INTERVAL_MINUTES} minutes.")
        print("Press Ctrl+C to terminate.\n")

        # Initial sweep immediately
        run_sweep(notifier)

        schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(run_sweep, notifier=notifier)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        # Default behavior: run one sweep
        run_sweep(notifier)
        print("\n💡 Tip: To run on a schedule in the background, run:")
        print("   python main.py --daemon")

if __name__ == "__main__":
    main()
