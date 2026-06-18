"""
gui/main_window.py

The top-level application window. Hosts the Dashboard, Scrape Website,
History, and Settings pages in a tabbed layout, and owns the single
shared SQLite connection used by every page.
"""

from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon
import os

from gui.dashboard import DashboardPage
from gui.scraper_page import ScraperPage
from gui.history_page import HistoryPage
from gui.settings_page import SettingsPage
from utils.paths import get_resource_path


class MainWindow(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle("WebScraper Pro")
        self.resize(1100, 720)

        # Set window icon
        icon_path = get_resource_path(os.path.join("assets", "icons", "app.png"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard_page = DashboardPage(conn)
        self.history_page = HistoryPage(conn)
        self.scraper_page = ScraperPage(conn, on_scrape_saved=self._on_data_changed)
        self.settings_page = SettingsPage()

        self.tabs.addTab(self.dashboard_page, "Dashboard")
        self.tabs.addTab(self.scraper_page, "Scrape Website")
        self.tabs.addTab(self.history_page, "History")
        self.tabs.addTab(self.settings_page, "Settings")

        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _on_data_changed(self):
        """Called after a new scrape is saved, so other tabs reflect it."""
        self.dashboard_page.refresh()
        self.history_page.refresh()

    def _on_tab_changed(self, index):
        widget = self.tabs.widget(index)
        if widget is self.dashboard_page:
            self.dashboard_page.refresh()
        elif widget is self.history_page:
            self.history_page.refresh()
