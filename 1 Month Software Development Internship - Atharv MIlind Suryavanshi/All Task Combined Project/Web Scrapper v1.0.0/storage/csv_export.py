"""
storage/csv_export.py

Exports scraped website summaries to CSV, either as a single new file
or appended to an existing one (useful for building up a running log).
"""

import csv
import os
from typing import Iterable, Union

from database.models import ScrapedWebsite

FIELDNAMES = ["URL", "Title", "Links", "Images", "Headings", "Status Code", "Date"]


def _row_for(site: ScrapedWebsite) -> dict:
    return {
        "URL": site.url,
        "Title": site.title,
        "Links": len(site.links),
        "Images": len(site.images),
        "Headings": len(site.headings),
        "Status Code": site.status_code,
        "Date": site.scrape_date,
    }


def export_csv(site_or_sites: Union[ScrapedWebsite, Iterable[ScrapedWebsite]], filepath: str, append: bool = False) -> None:
    """
    Write one ScrapedWebsite, or an iterable of them, as CSV rows to `filepath`.
    If append=True and the file already exists, new rows are added without
    rewriting the header.
    """
    if isinstance(site_or_sites, ScrapedWebsite):
        sites = [site_or_sites]
    else:
        sites = list(site_or_sites)

    file_exists = append and os.path.isfile(filepath)
    mode = "a" if append else "w"

    with open(filepath, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        for site in sites:
            writer.writerow(_row_for(site))
