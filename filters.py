from typing import Tuple, List
import config

def evaluate_legitimacy(title: str, text: str, url: str, upvotes: int = 0) -> Tuple[int, bool, List[str]]:
    """
    Evaluates the legitimacy of an earning opportunity.
    Returns:
        (score: int, is_legit: bool, flags: List[str])
    """
    score = 50  # Start at neutral baseline
    flags = []
    combined = f"{title.lower()} {text.lower()} {url.lower()}"

    # 1. Critical Scam Keyword Check
    for scam_word in config.SCAM_KEYWORDS:
        if scam_word in combined:
            score -= 60
            flags.append(f"⛔ Scam trigger detected: '{scam_word}'")

    # 2. Deceptive Scheme Checks (Targeting scam investments, NOT free earning bots)
    if "whatsapp" in combined and ("chat" in combined or "dm" in combined or "admin" in combined):
        score -= 40
        flags.append("⛔ Suspicious WhatsApp contact redirection")

    if ("telegram investment" in combined or "crypto multiplier" in combined or "forex signals" in combined or "send crypto to bot" in combined):
        score -= 50
        flags.append("⛔ Suspicious Telegram investment/doubler scheme")

    if "guaranteed" in combined and ("daily" in combined or "instant" in combined or "passive" in combined):
        score -= 25
        flags.append("⚠️ Unrealistic guarantee claims")

    # 3. FCFS (First-Come First-Served) & Signup Bonus Detection & Boost
    fcfs_signals = ["fcfs", "first come first serve", "first 100", "first 500", "first 1000", "early bird", "early access reward"]
    signup_signals = ["signup bonus", "sign up bonus", "register bonus", "registration bonus", "free registration reward"]
    
    is_fcfs = any(sig in combined for sig in fcfs_signals)
    if is_fcfs:
        score += 15
        flags.append("⚡ FCFS (First-Come, First-Served) - Limited spots!")

    if any(sig in combined for sig in signup_signals):
        score += 15
        flags.append("🎁 Verified Signup / Registration Reward")

    # 4. Telegram Earning Bot & Mini-App Signals
    if "t.me/" in url.lower() or "telegram bot" in combined or "mini app" in combined:
        if "deposit" in combined or "invest" in combined:
            score -= 40
            flags.append("⛔ Telegram bot asks for deposit/investment")
        else:
            score += 15
            flags.append("🤖 Free Telegram Bot / Mini-App Task")

    # 3. Trusted Platform / Domain Boosts
    for trusted in config.TRUSTED_PLATFORMS:
        if trusted in url.lower() or trusted in combined:
            score += 35
            flags.append(f"✅ Verified trusted platform match: {trusted}")
            break

    # 4. Community Upvotes / Signals
    if upvotes >= 20:
        score += 20
        flags.append(f"✅ Strong community endorsement ({upvotes}+ upvotes)")
    elif upvotes >= 5:
        score += 10
        flags.append(f"✅ Positive community score ({upvotes} upvotes)")

    # 5. Legitimate Payment Methods Mentioned
    legit_payouts = ["paypal", "direct deposit", "stripe", "bank transfer", "wise", "gift card (amazon)"]
    for payout in legit_payouts:
        if payout in combined:
            score += 10
            flags.append(f"✅ Standard payout method: {payout.title()}")
            break

    # 6. Explicitly No Cost / Free
    if "no fee" in combined or "free to apply" in combined or "no purchase" in combined or "free to join" in combined:
        score += 10
        flags.append("✅ Confirmed zero upfront cost")

    # Clamp score between 0 and 100
    score = max(0, min(100, score))
    is_legit = score >= config.MIN_LEGITIMACY_SCORE and not any(f.startswith("⛔") for f in flags)

    return score, is_legit, flags
