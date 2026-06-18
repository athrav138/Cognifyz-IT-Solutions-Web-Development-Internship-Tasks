"""
scraper/parser.py

Takes raw HTML (plus the page URL, for resolving relative links) and
extracts the structured information WebScraper Pro cares about: title,
meta description, headings, links, and images.
"""

from datetime import datetime
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from database.models import ScrapedWebsite, Heading, ImageItem
from scraper.engine import FetchResult


def _absolute_url(base_url: str, link: str) -> str:
    try:
        return urljoin(base_url, link)
    except Exception:
        return link


def parse_html(fetch_result: FetchResult, max_links: int = 0, max_images: int = 0) -> ScrapedWebsite:
    """
    Parse the HTML in `fetch_result` into a ScrapedWebsite object.

    max_links / max_images of 0 means "no limit" (caller can pass the
    user's Settings values to cap how much is stored, matching the
    "Maximum links" / "Maximum images" settings in the spec).
    """
    soup = BeautifulSoup(fetch_result.html, "lxml")

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "(No title found)"

    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()

    headings = []
    for level in range(1, 7):
        for tag in soup.find_all(f"h{level}"):
            text = tag.get_text(strip=True)
            if text:
                headings.append(Heading(tag=f"H{level}", text=text))

    seen_links = set()
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        absolute = _absolute_url(fetch_result.url, href)
        if absolute not in seen_links:
            seen_links.add(absolute)
            links.append(absolute)
            if max_links and len(links) >= max_links:
                break

    seen_images = set()
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        absolute = _absolute_url(fetch_result.url, src.strip())
        if absolute not in seen_images:
            seen_images.add(absolute)
            images.append(ImageItem(image_url=absolute, alt_text=img.get("alt", "") or ""))
            if max_images and len(images) >= max_images:
                break

    return ScrapedWebsite(
        url=fetch_result.url,
        title=title,
        description=description,
        status_code=fetch_result.status_code,
        response_time=fetch_result.response_time,
        content_type=fetch_result.content_type,
        server=fetch_result.server,
        page_size=fetch_result.page_size,
        scrape_date=datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        headings=headings,
        links=links,
        images=images,
    )
