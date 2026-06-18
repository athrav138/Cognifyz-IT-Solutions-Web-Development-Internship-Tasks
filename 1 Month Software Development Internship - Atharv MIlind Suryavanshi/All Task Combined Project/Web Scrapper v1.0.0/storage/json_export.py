"""
storage/json_export.py

Exports a single scraped website (or a list of them) to a JSON file,
suitable for backups, API consumption, or feeding into other tools.
"""

import json
from typing import Iterable, Union

from database.models import ScrapedWebsite


def export_json(site_or_sites: Union[ScrapedWebsite, Iterable[ScrapedWebsite]], filepath: str) -> None:
    """
    Write one ScrapedWebsite, or an iterable of them, as JSON to `filepath`.
    """
    if isinstance(site_or_sites, ScrapedWebsite):
        data = site_or_sites.to_dict()
    else:
        data = [site.to_dict() for site in site_or_sites]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
