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
    {"name": "ISNA", "url": "https://www.isna.ir/rss/tp/9"},
    {"name": "مهر", "url": "https://www.mehrnews.com/rss/tp/12"},
    {"name": "ایرنا", "url": "https://www.irna.ir/rss"},
{"name": "خبرآنلاین", "url": "https://www.khabaronline.ir/rss"},
    {"name": "مهر ورزشی", "url": "https://www.mehrnews.com/rss/tp/14"},
]

# ── Climbing keywords (Farsi + English for mixed content) ──────
# Only specific climbing terms — generic words like "ارتفاع" and "صعود" cause false positives
CLIMBING_KEYWORDS = [
    # کوهنوردی (very specific)
    "کوهنوردی", "کوهنورد",
    "سنگ‌نوردی", "سنگنوردی", "سنگ نوردی", "صخره‌نوردی",
    "دیواره‌نوردی", "دیواره نوردی",
    "یخ‌نوردی", "یخ نوردی",
    # صعود خاص
    "صعود به قله", "صعود زمستانه", "صعود از مسیر",
    "فتح قله", "قله‌نوردی",
    # حوادث کوه
    "حوادث کوه", "حوادث کوهستان", "سقوط از کوه",
    "گم شدن در کوه", "گم شدن در ارتفاعات",
    "امداد کوهستان", "نجات کوهستان", "امداد کوهنورد",
    "تیم امداد کوه", "عملیات امداد کوهستان",
    # تجهیزات
    "کارابین", "طناب کوهنوردی", "گلایدر کوهنوردی",
    # رشته‌کوه‌ها (keep these — specific enough in context)
    "البرز", "زاگرس", "دماوند", "سبلان","رشته کوه البرز , " رشته کوه زاگرس" , "قله سبلان", "قله دماوند"
    "هیمالیا",
    # پناهگاه و اصطلاحات
    "پناهگاه کوهستان" ,
    # English
    "ice climbing", "mountaineering", "mountain rescue",
    "rock climbing", "alpine", "summit", "climbing expedition",
]


def is_climbing_related(title: str, summary: str) -> bool:
    """Check if news item is climbing-related."""
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in CLIMBING_KEYWORDS)


def format_message(title: str, summary: str, source: str, url: str, pub_date: str = "") -> str:
    """Format a Telegram message with Persian styling."""
    msg = f"🏔️ <b>{title}</b>\n\n"
    if summary:
        msg += f"{summary}\n\n"
    if pub_date:
        msg += f"🕒 {pub_date}\n"
    msg += f"📰 {source}\n"
    msg += f"🔗 <a href=\"{url}\">لینک خبر</a>\n\n"
    msg += "━━━━━━━━━━━━━━━\n"
    msg += "🏔️ کوهنامه | koohnameh.ir"
    return msg


def format_no_news_message() -> str:
    """Message when no climbing news found."""
    return (
        "🏔️ <b>کوهنامه</b>\n\n"
        "خبر جدیدی درباره کوهنوردی و حوادث کوهستان یافت نشد.\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🏔️ کوهنامه | koohnameh.ir"
    )
