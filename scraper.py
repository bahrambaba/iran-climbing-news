"""RSS scraper: fetch Iranian news, filter climbing-related."""

import xml.etree.ElementTree as ET
import urllib.request
import ssl
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

from config import SOURCES, is_climbing_related

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
CTX = ssl.create_default_context()


@dataclass
class NewsItem:
    title: str
    url: str
    summary: str
    source: str
    pub_date: str = ""
    image_url: str = ""

    def to_dict(self):
        return asdict(self)


def fetch_feed(url: str, source_name: str) -> list[NewsItem]:
    """Fetch and parse an RSS feed."""
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=20, context=CTX).read()
        root = ET.fromstring(data)

        for item_el in root.iter("item"):
            title = (item_el.findtext("title") or "").strip()
            link = (item_el.findtext("link") or "").strip()
            desc = (item_el.findtext("description") or "").strip()
            pub = (item_el.findtext("pubDate") or "").strip()

            # Try to get image from <enclosure>
            img = ""
            enc = item_el.find("enclosure")
            if enc is not None:
                img = enc.get("url", "")

            if title and link:
                items.append(NewsItem(
                    title=title,
                    url=link,
                    summary=desc,
                    source=source_name,
                    pub_date=pub,
                    image_url=img,
                ))
    except Exception as e:
        print(f"[WARN] Failed to fetch {source_name}: {e}")

    return items


def scrape_all() -> list[NewsItem]:
    """Fetch all sources and filter for climbing news."""
    climbing_news = []
    for src in SOURCES:
        items = fetch_feed(src["url"], src["name"])
        for item in items:
            if is_climbing_related(item.title, item.summary):
                climbing_news.append(item)
    return climbing_news
