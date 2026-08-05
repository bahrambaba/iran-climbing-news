"""Telegram Bot API sender."""

import requests
import time

from config import BOT_TOKEN, CHAT_ID


def send_message(text: str) -> bool:
    """Send a text message to Telegram."""
    if not BOT_TOKEN or not CHAT_ID:
        print("[ERROR] BOT_TOKEN or CHAT_ID not set")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "false",
    }, timeout=30)

    if resp.status_code == 200:
        return True
    print(f"[ERROR] sendMessage: {resp.status_code} {resp.text[:200]}")
    return False


def send_photo(photo_url: str, caption: str) -> bool:
    """Send a photo with caption to Telegram."""
    if not BOT_TOKEN or not CHAT_ID:
        print("[ERROR] BOT_TOKEN or CHAT_ID not set")
        return False

    # Telegram caption limit is 1024 chars
    if len(caption) > 1024:
        return send_message(caption)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    resp = requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML",
    }, timeout=30)

    if resp.status_code == 200:
        return True
    # Fallback to text if photo fails
    print(f"[WARN] sendPhoto failed: {resp.status_code}, falling back to text")
    return send_message(caption)


def send_news_batch(news_items: list) -> int:
    """Send a list of news items. Returns count of sent items."""
    sent = 0
    for item in news_items:
        from config import format_message
        text = format_message(
            title=item.title,
            summary=item.summary,
            source=item.source,
            url=item.url,
            pub_date=item.pub_date,
        )

        if item.image_url:
            ok = send_photo(item.image_url, text)
        else:
            ok = send_message(text)

        if ok:
            sent += 1
            time.sleep(1)  # Rate limit

    return sent
