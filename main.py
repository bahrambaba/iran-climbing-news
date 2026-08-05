"""Main: scrape → filter → dedup → send → Telegram."""

import json
import os
from datetime import datetime, timedelta, timezone

from config import SEEN_FILE, MAX_SEEN_AGE_HOURS, format_no_news_message
from scraper import scrape_all
from sender import send_message, send_news_batch


def load_seen() -> dict:
    """Load seen URLs with timestamps."""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_seen(seen: dict):
    """Save seen URLs."""
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)


def prune_seen(seen: dict, max_hours: int) -> dict:
    """Remove entries older than max_hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_hours)
    return {url: ts for url, ts in seen.items()
            if datetime.fromisoformat(ts) > cutoff}


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting crawl...")

    # Scrape and filter
    news = scrape_all()
    print(f"  Found {len(news)} climbing-related items")

    # Dedup
    seen = load_seen()
    seen = prune_seen(seen, MAX_SEEN_AGE_HOURS)
    new_items = [item for item in news if item.url not in seen]

    if not new_items:
        print("  No new items")
        msg = format_no_news_message()
        send_message(msg)
        return

    print(f"  Sending {len(new_items)} new items")
    sent = send_news_batch(new_items)

    # Mark as seen
    for item in new_items:
        seen[item.url] = datetime.now(timezone.utc).isoformat()
    save_seen(seen)

    print(f"  Done: {sent}/{len(new_items)} sent")


if __name__ == "__main__":
    main()
