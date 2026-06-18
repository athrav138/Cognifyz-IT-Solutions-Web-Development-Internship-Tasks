"""
storage/txt_export.py

Generates a human-readable TXT report for a single scraped website,
matching the format shown in the project spec.
"""

from database.models import ScrapedWebsite


def build_txt_report(site: ScrapedWebsite) -> str:
    lines = []
    lines.append("=" * 48)
    lines.append("              WEB SCRAPING REPORT")
    lines.append("=" * 48)
    lines.append("")
    lines.append("URL:")
    lines.append(site.url)
    lines.append("")
    lines.append("Date:")
    lines.append(site.scrape_date)
    lines.append("")
    lines.append("")
    lines.append("TITLE")
    lines.append("-" * 48)
    lines.append(site.title or "(No title found)")
    lines.append("")
    lines.append("")

    if site.description:
        lines.append("META DESCRIPTION")
        lines.append("-" * 48)
        lines.append(site.description)
        lines.append("")
        lines.append("")

    lines.append("HEADINGS")
    lines.append("-" * 48)
    lines.append("")
    if site.headings:
        for idx, h in enumerate(site.headings, start=1):
            lines.append(f"{idx}. [{h.tag}] {h.text}")
    else:
        lines.append("(No headings found)")
    lines.append("")
    lines.append("")

    lines.append("LINKS")
    lines.append("-" * 48)
    lines.append("")
    if site.links:
        for idx, link in enumerate(site.links, start=1):
            lines.append(f"{idx}. {link}")
    else:
        lines.append("(No links found)")
    lines.append("")
    lines.append("")

    lines.append("IMAGES")
    lines.append("-" * 48)
    lines.append("")
    if site.images:
        for idx, img in enumerate(site.images, start=1):
            alt = f" (alt: {img.alt_text})" if img.alt_text else ""
            lines.append(f"{idx}. {img.image_url}{alt}")
    else:
        lines.append("(No images found)")
    lines.append("")
    lines.append("")

    lines.append("STATISTICS")
    lines.append("-" * 48)
    lines.append("")
    lines.append(f"Total Headings: {len(site.headings)}")
    lines.append(f"Total Links: {len(site.links)}")
    lines.append(f"Total Images: {len(site.images)}")
    lines.append(f"HTTP Status Code: {site.status_code}")
    lines.append(f"Response Time: {site.response_time} seconds")
    lines.append(f"Page Size: {site.page_size} bytes")
    lines.append(f"Content Type: {site.content_type}")
    lines.append(f"Server: {site.server}")
    lines.append("")
    lines.append("")
    lines.append("END OF REPORT")
    lines.append("=" * 48)

    return "\n".join(lines)


def export_txt(site: ScrapedWebsite, filepath: str) -> None:
    """Write the TXT report for `site` to `filepath`."""
    content = build_txt_report(site)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
