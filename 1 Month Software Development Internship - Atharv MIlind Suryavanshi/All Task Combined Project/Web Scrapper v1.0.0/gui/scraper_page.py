"""
gui/scraper_page.py

The main "Scrape Website" screen. Lets the user enter a URL, runs the
scrape on a background QThread (so the UI never freezes), shows the
results, and lets the user save a TXT report or export JSON/CSV.
Every successful scrape is also written to the database automatically
so it shows up in History.
"""

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QGroupBox, QGridLayout, QMessageBox, QFileDialog, QMenu
)

from scraper.engine import fetch_url, ScraperError
from scraper.parser import parse_html
from database import queries
from storage.txt_export import export_txt
from storage.json_export import export_json
from storage.csv_export import export_csv
from storage.pdf_export import export_pdf
from utils.config import load_settings

import os


class ScrapeWorker(QThread):
    """Runs the network request + parsing off the GUI thread."""
    succeeded = pyqtSignal(object)   # ScrapedWebsite
    failed = pyqtSignal(str)         # error message

    def __init__(self, url: str, settings: dict):
        super().__init__()
        self.url = url
        self.settings = settings

    def run(self):
        try:
            result = fetch_url(
                self.url,
                timeout=self.settings.get("timeout", 10),
                user_agent=self.settings.get("user_agent", "Mozilla/5.0"),
            )
            site = parse_html(
                result,
                max_links=self.settings.get("max_links", 0),
                max_images=self.settings.get("max_images", 0),
            )
            self.succeeded.emit(site)
        except ScraperError as e:
            self.failed.emit(e.message)
        except Exception as e:  # pragma: no cover - safety net
            self.failed.emit(f"Unexpected error: {e}")


class ScraperPage(QWidget):
    def __init__(self, conn, on_scrape_saved=None):
        super().__init__()
        self.conn = conn
        self.on_scrape_saved = on_scrape_saved  # callback to refresh dashboard/history
        self.current_site = None
        self.worker = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Scrape Website")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        url_row = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.url_input.returnPressed.connect(self.start_scraping)
        self.scrape_btn = QPushButton("Start Scraping")
        self.scrape_btn.setObjectName("PrimaryButton")
        self.scrape_btn.clicked.connect(self.start_scraping)
        url_row.addWidget(self.url_input)
        url_row.addWidget(self.scrape_btn)
        layout.addLayout(url_row)

        self.status_label = QLabel("")
        self.status_label.setObjectName("StatusLabel")
        layout.addWidget(self.status_label)

        info_group = QGroupBox("Website Information")
        info_grid = QGridLayout(info_group)
        self.title_value = QLabel("-")
        self.title_value.setWordWrap(True)
        self.desc_value = QLabel("-")
        self.desc_value.setWordWrap(True)
        self.stats_value = QLabel("-")
        info_grid.addWidget(QLabel("Title:"), 0, 0)
        info_grid.addWidget(self.title_value, 0, 1)
        info_grid.addWidget(QLabel("Meta Description:"), 1, 0)
        info_grid.addWidget(self.desc_value, 1, 1)
        info_grid.addWidget(QLabel("Stats:"), 2, 0)
        info_grid.addWidget(self.stats_value, 2, 1)
        info_grid.setColumnStretch(1, 1)
        layout.addWidget(info_group)

        results_row = QHBoxLayout()

        headings_group = QGroupBox("Headings")
        headings_layout = QVBoxLayout(headings_group)
        self.headings_box = QTextEdit()
        self.headings_box.setReadOnly(True)
        headings_layout.addWidget(self.headings_box)
        results_row.addWidget(headings_group)

        links_group = QGroupBox("Links")
        links_layout = QVBoxLayout(links_group)
        self.links_box = QTextEdit()
        self.links_box.setReadOnly(True)
        links_layout.addWidget(self.links_box)
        results_row.addWidget(links_group)

        images_group = QGroupBox("Images")
        images_layout = QVBoxLayout(images_group)
        self.images_box = QTextEdit()
        self.images_box.setReadOnly(True)
        images_layout.addWidget(self.images_box)
        results_row.addWidget(images_group)

        layout.addLayout(results_row, stretch=1)

        action_row = QHBoxLayout()
        action_row.addStretch()
        self.save_report_btn = QPushButton("Save Report (TXT)")
        self.save_report_btn.clicked.connect(self.save_report)
        self.save_report_btn.setEnabled(False)

        self.export_btn = QPushButton("Export Data ▾")
        self.export_btn.setEnabled(False)
        export_menu = QMenu(self.export_btn)
        export_menu.addAction("Export as JSON", lambda: self.export_data("json"))
        export_menu.addAction("Export as CSV", lambda: self.export_data("csv"))
        export_menu.addAction("Export as PDF", lambda: self.export_data("pdf"))
        self.export_btn.setMenu(export_menu)

        action_row.addWidget(self.save_report_btn)
        action_row.addWidget(self.export_btn)
        layout.addLayout(action_row)

    def start_scraping(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid website address.")
            return

        settings = load_settings()
        self.scrape_btn.setEnabled(False)
        self.scrape_btn.setText("Scraping...")
        self.status_label.setText(f"Sending request to {url} ...")
        self.save_report_btn.setEnabled(False)
        self.export_btn.setEnabled(False)

        self.worker = ScrapeWorker(url, settings)
        self.worker.succeeded.connect(self._on_success)
        self.worker.failed.connect(self._on_failure)
        self.worker.finished.connect(self._on_worker_finished)
        self.worker.start()

    def _on_worker_finished(self):
        self.scrape_btn.setEnabled(True)
        self.scrape_btn.setText("Start Scraping")

    def _on_success(self, site):
        self.current_site = site
        self.status_label.setText(
            f"Success — HTTP {site.status_code} — {site.response_time}s — {site.page_size} bytes"
        )

        self.title_value.setText(site.title or "(No title found)")
        self.desc_value.setText(site.description or "(No meta description found)")
        self.stats_value.setText(
            f"Headings: {len(site.headings)}   |   Links: {len(site.links)}   |   Images: {len(site.images)}"
        )

        self.headings_box.setPlainText(
            "\n".join(f"[{h.tag}] {h.text}" for h in site.headings) or "(No headings found)"
        )
        self.links_box.setPlainText("\n".join(site.links) or "(No links found)")
        self.images_box.setPlainText(
            "\n".join(i.image_url for i in site.images) or "(No images found)"
        )

        self.save_report_btn.setEnabled(True)
        self.export_btn.setEnabled(True)

        # Persist to the database automatically so it appears in History.
        try:
            queries.save_website(self.conn, site)
            if self.on_scrape_saved:
                self.on_scrape_saved()
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Unable to save data.\n\n{e}")

    def _on_failure(self, message):
        self.status_label.setText(f"Error: {message}")
        QMessageBox.critical(self, "Scraping Failed", message)

    def _default_filename(self, ext: str) -> str:
        if not self.current_site:
            return f"report.{ext}"
        safe = "".join(c if c.isalnum() else "_" for c in self.current_site.url)[:60]
        return f"{safe}.{ext}"

    def save_report(self):
        if not self.current_site:
            return
        settings = load_settings()
        default_path = os.path.join(settings.get("export_folder", "."), self._default_filename("txt"))
        path, _ = QFileDialog.getSaveFileName(self, "Save TXT Report", default_path, "Text Files (*.txt)")
        if not path:
            return
        try:
            export_txt(self.current_site, path)
            QMessageBox.information(self, "Saved", f"Report saved to:\n{path}")
        except OSError as e:
            QMessageBox.critical(self, "Save Failed", f"Unable to save report.\n\n{e}")

    def export_data(self, fmt: str):
        if not self.current_site:
            return
        settings = load_settings()
        default_path = os.path.join(settings.get("export_folder", "."), self._default_filename(fmt))
        if fmt == "json":
            path, _ = QFileDialog.getSaveFileName(self, "Export JSON", default_path, "JSON Files (*.json)")
            if not path:
                return
            try:
                export_json(self.current_site, path)
                QMessageBox.information(self, "Exported", f"Data exported to:\n{path}")
            except OSError as e:
                QMessageBox.critical(self, "Export Failed", f"Unable to export data.\n\n{e}")
        elif fmt == "csv":
            path, _ = QFileDialog.getSaveFileName(self, "Export CSV", default_path, "CSV Files (*.csv)")
            if not path:
                return
            try:
                export_csv(self.current_site, path)
                QMessageBox.information(self, "Exported", f"Data exported to:\n{path}")
            except OSError as e:
                QMessageBox.critical(self, "Export Failed", f"Unable to export data.\n\n{e}")
        elif fmt == "pdf":
            path, _ = QFileDialog.getSaveFileName(self, "Export PDF", default_path, "PDF Files (*.pdf)")
            if not path:
                return
            try:
                export_pdf(self.current_site, path)
                QMessageBox.information(self, "Exported", f"Data exported to:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Unable to export data.\n\n{e}")
