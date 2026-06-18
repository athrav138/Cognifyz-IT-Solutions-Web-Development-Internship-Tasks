"""
main.py

Entry point for WebScraper Pro. Initializes the SQLite database (creating
it on first run), applies the application stylesheet, builds the main
window, and starts the Qt event loop.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from database.connection import init_db, get_connection, DEFAULT_DB_PATH
from gui.main_window import MainWindow
from assets.themes.style import STYLESHEET


def main():
    init_db(DEFAULT_DB_PATH)
    conn = get_connection(DEFAULT_DB_PATH)

    app = QApplication(sys.argv)
    app.setApplicationName("WebScraper Pro")
    
    # Force a valid point size globally
    font = app.font()
    font.setPointSize(10)
    font.setFamily("Segoe UI")
    app.setFont(font)
    
    # Apply the modern stylesheet
    app.setStyleSheet(STYLESHEET)

    window = MainWindow(conn)
    window.show()

    exit_code = app.exec()
    conn.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
