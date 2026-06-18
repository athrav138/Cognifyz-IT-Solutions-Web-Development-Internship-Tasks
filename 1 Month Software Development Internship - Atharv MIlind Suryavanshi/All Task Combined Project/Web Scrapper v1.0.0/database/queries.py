"""
database/queries.py

All SQL operations used by the rest of the application live here, so the
GUI and other modules never need to write raw SQL.
"""

import sqlite3
from typing import List, Optional

from database.connection import get_connection
from database.models import ScrapedWebsite, Heading, ImageItem


def save_website(conn: sqlite3.Connection, site: ScrapedWebsite) -> int:
    """
    Insert a scraped website (and its headings/links/images) into the database.
    Returns the new website id. Raises sqlite3.Error on failure.
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO websites
            (url, title, description, status_code, response_time,
             content_type, server, page_size, scrape_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            site.url, site.title, site.description, site.status_code,
            site.response_time, site.content_type, site.server,
            site.page_size, site.scrape_date,
        ),
    )
    website_id = cur.lastrowid

    if site.headings:
        cur.executemany(
            "INSERT INTO headings (website_id, tag, text) VALUES (?, ?, ?)",
            [(website_id, h.tag, h.text) for h in site.headings],
        )

    if site.links:
        cur.executemany(
            "INSERT INTO links (website_id, link) VALUES (?, ?)",
            [(website_id, link) for link in site.links],
        )

    if site.images:
        cur.executemany(
            "INSERT INTO images (website_id, image_url, alt_text) VALUES (?, ?, ?)",
            [(website_id, img.image_url, img.alt_text) for img in site.images],
        )

    conn.commit()
    return website_id


def get_history(conn: sqlite3.Connection, limit: int = 200) -> List[sqlite3.Row]:
    """Return the most recent scraped websites, newest first."""
    cur = conn.execute(
        "SELECT * FROM websites ORDER BY id DESC LIMIT ?", (limit,)
    )
    return cur.fetchall()


def search_websites(conn: sqlite3.Connection, term: str) -> List[sqlite3.Row]:
    """Search history by URL or title (case-insensitive substring match)."""
    like_term = f"%{term}%"
    cur = conn.execute(
        """
        SELECT * FROM websites
        WHERE url LIKE ? OR title LIKE ?
        ORDER BY id DESC
        """,
        (like_term, like_term),
    )
    return cur.fetchall()


def get_website_detail(conn: sqlite3.Connection, website_id: int) -> Optional[ScrapedWebsite]:
    """Load a full ScrapedWebsite (with headings/links/images) by id."""
    row = conn.execute("SELECT * FROM websites WHERE id = ?", (website_id,)).fetchone()
    if row is None:
        return None

    site = ScrapedWebsite(
        url=row["url"],
        title=row["title"] or "",
        description=row["description"] or "",
        status_code=row["status_code"],
        response_time=row["response_time"],
        content_type=row["content_type"] or "",
        server=row["server"] or "",
        page_size=row["page_size"] or 0,
        scrape_date=row["scrape_date"],
        id=row["id"],
    )

    for h in conn.execute("SELECT tag, text FROM headings WHERE website_id = ?", (website_id,)):
        site.headings.append(Heading(tag=h["tag"], text=h["text"]))

    for l in conn.execute("SELECT link FROM links WHERE website_id = ?", (website_id,)):
        site.links.append(l["link"])

    for i in conn.execute("SELECT image_url, alt_text FROM images WHERE website_id = ?", (website_id,)):
        site.images.append(ImageItem(image_url=i["image_url"], alt_text=i["alt_text"] or ""))

    return site


def delete_website(conn: sqlite3.Connection, website_id: int) -> None:
    """Delete a single website and its related rows (cascades via FK)."""
    conn.execute("DELETE FROM websites WHERE id = ?", (website_id,))
    conn.commit()


def delete_all_history(conn: sqlite3.Connection) -> None:
    """Wipe every record from every table."""
    conn.execute("DELETE FROM images")
    conn.execute("DELETE FROM links")
    conn.execute("DELETE FROM headings")
    conn.execute("DELETE FROM websites")
    conn.commit()


def get_dashboard_stats(conn: sqlite3.Connection) -> dict:
    """Aggregate counts used by the Dashboard page."""
    total_websites = conn.execute("SELECT COUNT(*) FROM websites").fetchone()[0]
    total_links = conn.execute("SELECT COUNT(*) FROM links").fetchone()[0]
    total_images = conn.execute("SELECT COUNT(*) FROM images").fetchone()[0]

    last_row = conn.execute(
        "SELECT url, scrape_date FROM websites ORDER BY id DESC LIMIT 1"
    ).fetchone()

    return {
        "total_websites": total_websites,
        "total_links": total_links,
        "total_images": total_images,
        "last_url": last_row["url"] if last_row else None,
        "last_date": last_row["scrape_date"] if last_row else None,
    }
