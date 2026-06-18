"""
storage/pdf_export.py

Generates a professional PDF report for a single scraped website
using the fpdf2 library.
"""

from fpdf import FPDF
from database.models import ScrapedWebsite


class ScrapePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "WebScraper Pro - Scrape Report", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def export_pdf(site: ScrapedWebsite, filepath: str) -> None:
    pdf = ScrapePDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Website info
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(37, 99, 235) # Blue
    pdf.cell(0, 10, site.title or "(No Title)", ln=True)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"URL: {site.url}", ln=True)
    pdf.cell(0, 7, f"Scrape Date: {site.scrape_date}", ln=True)
    pdf.cell(0, 7, f"Status: {site.status_code} | Time: {site.response_time}s | Size: {site.page_size} bytes", ln=True)
    pdf.ln(5)

    # Description
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Meta Description:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, site.description or "(No description found)")
    pdf.ln(5)

    # Stats Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Summary Stats:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, f"- Total Headings: {len(site.headings)}", ln=True)
    pdf.cell(0, 7, f"- Total Links: {len(site.links)}", ln=True)
    pdf.cell(0, 7, f"- Total Images: {len(site.images)}", ln=True)
    pdf.ln(5)

    # Headings Section
    if site.headings:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Headings Found:", ln=True)
        pdf.set_font("Helvetica", "", 9)
        for h in site.headings[:50]: # Cap to avoid massive PDFs
            pdf.cell(10, 6, f"{h.tag}:", border=0)
            pdf.multi_cell(0, 6, h.text)
        if len(site.headings) > 50:
            pdf.cell(0, 6, f"... and {len(site.headings) - 50} more headings", ln=True)
        pdf.ln(5)

    # Links Section
    if site.links:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Links (First 50):", ln=True)
        pdf.set_font("Helvetica", "", 8)
        for link in site.links[:50]:
            pdf.cell(0, 5, link, ln=True)
        if len(site.links) > 50:
            pdf.cell(0, 6, f"... and {len(site.links) - 50} more links", ln=True)
        pdf.ln(5)

    pdf.output(filepath)
