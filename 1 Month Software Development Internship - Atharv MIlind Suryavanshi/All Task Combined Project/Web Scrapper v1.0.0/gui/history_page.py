"""
gui/history_page.py

Lets the user browse previously scraped websites, search by URL/title,
view full details for a record, and delete one or all records.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QTextEdit, QAbstractItemView
)
from PyQt6.QtCore import Qt

from database import queries


class DetailDialog(QDialog):
    """Read-only popup showing the full scrape detail for one record."""
    def __init__(self, site, parent=None):
        super().__init__(parent)
        self.setWindowTitle(site.url)
        self.resize(640, 520)
        layout = QVBoxLayout(self)

        header = QLabel(f"<b>{site.title or '(No title)'}</b><br>{site.url}<br>{site.scrape_date}")
        header.setWordWrap(True)
        layout.addWidget(header)

        stats = QLabel(
            f"Headings: {len(site.headings)}   Links: {len(site.links)}   "
            f"Images: {len(site.images)}   Status: {site.status_code}   "
            f"Response time: {site.response_time}s"
        )
        layout.addWidget(stats)

        text = QTextEdit()
        text.setReadOnly(True)
        body_lines = ["HEADINGS", "-" * 40]
        body_lines += [f"[{h.tag}] {h.text}" for h in site.headings] or ["(none)"]
        body_lines += ["", "LINKS", "-" * 40]
        body_lines += site.links or ["(none)"]
        body_lines += ["", "IMAGES", "-" * 40]
        body_lines += [i.image_url for i in site.images] or ["(none)"]
        text.setPlainText("\n".join(body_lines))
        layout.addWidget(text)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class HistoryPage(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Scraping History")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by URL or title...")
        self.search_input.returnPressed.connect(self.do_search)
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.do_search)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.refresh)
        search_row.addWidget(self.search_input)
        search_row.addWidget(search_btn)
        search_row.addWidget(clear_btn)
        layout.addLayout(search_row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Website", "Title", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.view_selected)
        layout.addWidget(self.table)

        action_row = QHBoxLayout()
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(self.view_selected)
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_selected)
        delete_all_btn = QPushButton("Delete All History")
        delete_all_btn.setObjectName("DangerButton")
        delete_all_btn.clicked.connect(self.delete_all)
        action_row.addWidget(view_btn)
        action_row.addWidget(delete_btn)
        action_row.addStretch()
        action_row.addWidget(delete_all_btn)
        layout.addLayout(action_row)

    def _populate(self, rows):
        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(row["url"]))
            self.table.setItem(r, 2, QTableWidgetItem(row["title"] or ""))
            self.table.setItem(r, 3, QTableWidgetItem(row["scrape_date"]))

    def refresh(self):
        self.search_input.clear()
        rows = queries.get_history(self.conn)
        self._populate(rows)

    def do_search(self):
        term = self.search_input.text().strip()
        if not term:
            self.refresh()
            return
        rows = queries.search_websites(self.conn, term)
        self._populate(rows)

    def _selected_id(self):
        selected = self.table.selectedItems()
        if not selected:
            return None
        row = selected[0].row()
        return int(self.table.item(row, 0).text())

    def view_selected(self):
        website_id = self._selected_id()
        if website_id is None:
            QMessageBox.information(self, "No Selection", "Select a record first.")
            return
        site = queries.get_website_detail(self.conn, website_id)
        if site is None:
            QMessageBox.warning(self, "Not Found", "That record no longer exists.")
            self.refresh()
            return
        DetailDialog(site, self).exec()

    def delete_selected(self):
        website_id = self._selected_id()
        if website_id is None:
            QMessageBox.information(self, "No Selection", "Select a record first.")
            return
        confirm = QMessageBox.question(
            self, "Delete Record", "Delete the selected website from history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                queries.delete_website(self.conn, website_id)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Unable to save data.\n\n{e}")

    def delete_all(self):
        confirm = QMessageBox.question(
            self, "Delete All History", "This will permanently delete ALL scraping history. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                queries.delete_all_history(self.conn)
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Unable to save data.\n\n{e}")
