"""Config: sources, keywords, message formatting."""

import os
import re
import unicodedata

# ── Telegram (set via GitHub Secrets) ──────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

# ── Seen URLs file (for dedup) ─────────────────────────────────
SEEN_FILE = "seen_urls.json"
MAX_SEEN_AGE_HOURS = 36

# ── Iranian news sources ───────────────────────────────────────
SOURCES = [
    {"name": "ISNA (دانشجویان)", "url": "https://www.isna.ir/rss/tp/9"},
    {"name": "مهر", "url": "https://www.mehrnews.com/rss/tp/12"},
    {"name": "ایرنا", "url": "https://www.irna.ir/rss"},
    {"name": "خبرآنلاین", "url": "https://www.khabaronline.ir/rss"},
    {"name": "مهر ورزشی", "url": "https://www.mehrnews.com/rss/tp/14"},
    {"name": "تابناک", "url": "https://www.tabnak.ir/fa/rss/allnews"},
    {"name": "همشهری آنلاین", "url": "https://www.hamshahrionline.ir/rss"},
    {"name": "همشهری ورزشی", "url": "https://www.hamshahrionline.ir/rss/tp/10"},
]

# ── Climbing keywords ───────────────────────────────────────────
# Tier 1: standalone terms — always match (very specific to climbing)
T1_KEYWORDS = [
    "کوهنوردی", "کوهنورد", "سنگ‌نوردی", "سنگنوردی", "سنگ نوردی",
    "صخره‌نوردی", "دیواره‌نوردی", "دیواره نوردی",
    "یخ‌نوردی", "یخ نوردی", "هیking",
    "mountaineering", "rock climbing", "ice climbing", "alpinism",
    "climbing expedition", "mountain rescue",
]

# Tier 2: multi-word phrases — always match
T2_KEYWORDS = [
    "صعود به قله", "صعود زمستانه", "صعود از مسیر", "فتح قله",
    "قله‌نوردی", "قله نوردی",
    "حوادث کوه", "حوادث کوهستان", "سقوط از کوه",
    "گم شدن در کوه", "گم شدن در ارتفاعات",
    "امداد کوهستان", "نجات کوهستان", "امداد کوهنورد",
    "تیم امداد کوه", "عملیات امداد کوهستان",
    "طناب کوهنوردی", "گلایدر کوهنوردی",
    "پناهگاه کوهستان",
]

# Tier 3: mountain names — only match when combined with climbing context words
T3_MOUNTAIN_NAMES = [
    "البرز", "زاگرس", "دماوند", "سبلان", "هیمالیا",
]
T3_CONTEXT_WORDS = [
    "کوه", "قله", "صعود", "دیواره", "سنگ", "یخ", "ارتفاع",
    "جلوه", "پناهگاه", "گردنه", "طناب", "کلاه", "باد", "برف",
    "سرما", "خطر", "سقوط", "گم", "امداد", "نجات", "نجات کوهستان",
    "ورزش", "اسپورت",
]


def is_climbing_related(title: str, summary: str) -> bool:
    """Check if news item is climbing-related.

    Tier 1: standalone climbing terms → match
    Tier 2: multi-word climbing phrases → match
    Tier 3: mountain names → match only if a climbing context word also present
    """
    text = (title + " " + summary).lower()

    # T1: standalone
    if any(kw.lower() in text for kw in T1_KEYWORDS):
        return True

    # T2: multi-word phrases
    if any(kw.lower() in text for kw in T2_KEYWORDS):
        return True

    # T3: mountain name + context word
    has_mountain = any(kw.lower() in text for kw in T3_MOUNTAIN_NAMES)
    has_context = any(kw.lower() in text for kw in T3_CONTEXT_WORDS)
    if has_mountain and has_context:
        return True

    return False


def format_message(title: str, summary: str, source: str, url: str, pub_date: str = "") -> str:
    """Format a Telegram message with Persian styling."""
    msg = f"🏔️ <b>{title}</b>\n\n"
    if summary:
        msg += f"{summary}\n\n"
    msg += f"📰 {source}\n"
    msg += f"🔗 <a href=\"{url}\">لینک خبر</a>\n\n"
    msg += "━━━━━━━━━━━━━━━\n"
    msg += "🏔️ کوهنامه | koohnameh.ir"
    return msg


def format_no_news_message() -> str:
    """Message when no climbing news found."""
    return (
        "🏔️ <b>کوهنامه</b>\n\n"
        "خبر جدیدی درباره کوهنوردی و حوادث کوهستان در سایت های خبری ایرانی یافت نشد.\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🏔️ کوهنامه | koohnameh.ir"
    )
