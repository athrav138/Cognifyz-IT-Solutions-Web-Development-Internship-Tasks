"""
database/models.py

Simple dataclasses representing the rows of each table.
These are used to pass scraped data around in a structured way
before it is written to the database or exported to files.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Heading:
    tag: str
    text: str


@dataclass
class ImageItem:
    image_url: str
    alt_text: str = ""


@dataclass
class ScrapedWebsite:
    """In-memory representation of a single scrape result."""
    url: str
    title: str = ""
    description: str = ""
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    content_type: str = ""
    server: str = ""
    page_size: int = 0
    scrape_date: str = ""

    headings: List[Heading] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    images: List[ImageItem] = field(default_factory=list)

    # Database id, populated after insert / when loaded from history
    id: Optional[int] = None

    def to_dict(self) -> dict:
        """Flat dict representation, convenient for JSON/CSV export."""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "status_code": self.status_code,
            "response_time": self.response_time,
            "content_type": self.content_type,
            "server": self.server,
            "page_size": self.page_size,
            "scrape_date": self.scrape_date,
            "headings": [{"tag": h.tag, "text": h.text} for h in self.headings],
            "links": list(self.links),
            "images": [{"image_url": i.image_url, "alt_text": i.alt_text} for i in self.images],
            "total_headings": len(self.headings),
            "total_links": len(self.links),
            "total_images": len(self.images),
        }
