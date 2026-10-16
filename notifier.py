import html
import requests
from typing import Optional
import config
from searchers.base import Opportunity

class TelegramNotifier:
    """Delivers opportunity alerts directly to Telegram channel or direct chat"""

    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self._bot_token = bot_token
        self._chat_id = chat_id

    @property
    def token(self) -> str:
        return (self._bot_token or config.get_telegram_token()).strip()

    @property
    def chat(self) -> str:
        return (self._chat_id or config.get_telegram_chat_id()).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.token and self.chat)

    def test_connection(self) -> dict:
        """Verifies Telegram Bot Token validity against Telegram API."""
        if not self.token:
            return {"ok": False, "error": "Bot token not provided"}
        try:
            url = f"https://api.telegram.org/bot{self.token}/getMe"
            resp = requests.get(url, timeout=10)
            return resp.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_message(self, text: str) -> bool:
        """Sends raw text or HTML message via Telegram."""
        if not self.is_configured:
            print(f"[Console Alert]:\n{text}\n")
            return True

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }

        try:
            resp = requests.post(url, json=payload, timeout=12)
            data = resp.json()
            if not data.get("ok"):
                print(f"[Telegram Error] {data.get('description')}")
                return False
            return True
        except Exception as e:
            print(f"[Telegram Network Error] {e}")
            return False

    def send_message_detailed(self, text: str) -> dict:
        """Sends message and returns detailed Telegram API response for debugging."""
        if not self.token:
            return {"ok": False, "error": "TELEGRAM_BOT_TOKEN is empty"}
        if not self.chat:
            return {"ok": False, "error": "TELEGRAM_CHAT_ID is empty"}

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }

        try:
            resp = requests.post(url, json=payload, timeout=12)
            return resp.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_opportunity(self, opp: Opportunity) -> bool:
        """Formats and sends an opportunity card to Telegram."""
        safe_title = html.escape(opp.title)
        safe_link = html.escape(opp.link)
        safe_source = html.escape(opp.source)
        safe_category = html.escape(opp.category)
        safe_snippet = html.escape(opp.snippet) if opp.snippet else "No snippet provided."

        # Header badges
        badges = []
        if any("FCFS" in f for f in opp.flags):
            badges.append("⚡ <b>[FCFS - ACT FAST! LIMITED SPOTS]</b>")
        if "Telegram" in opp.category or "t.me/" in opp.link or any("Telegram" in f for f in opp.flags):
            badges.append("🤖 <b>[TELEGRAM BOT / MINI-APP]</b>")
        badge_header = ("\n".join(badges) + "\n\n") if badges else ""

        score_bar = "🟢" if opp.score >= 70 else "🟡"
        flags_text = ""
        if opp.flags:
            flags_text = "\n" + "\n".join([f"  • {html.escape(f)}" for f in opp.flags[:3]])

        message = (
            f"{badge_header}🎯 <b>NEW LEGIT EARNING OPPORTUNITY</b>\n\n"
            f"<b>Title:</b> <a href=\"{safe_link}\">{safe_title}</a>\n"
            f"📁 <b>Category:</b> {safe_category}\n"
            f"🌐 <b>Source:</b> {safe_source}\n"
            f"🛡️ <b>Legitimacy Score:</b> {score_bar} {opp.score}/100"
            f"{flags_text}\n\n"
            f"📝 <b>Summary:</b>\n<i>{safe_snippet}</i>\n\n"
            f"🔗 <a href=\"{safe_link}\">👉 Click Here to Open Link</a>"
        )

        return self.send_message(message)
