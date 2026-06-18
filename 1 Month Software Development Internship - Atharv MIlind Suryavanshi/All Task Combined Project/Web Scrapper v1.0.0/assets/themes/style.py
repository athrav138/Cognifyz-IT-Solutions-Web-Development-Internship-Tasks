"""
assets/themes/style.py

A sophisticated, dark modern stylesheet for WebScraper Pro.
Inspired by modern glassmorphic web aesthetics but built for PyQt6.
Uses point sizes (pt) for better cross-platform consistency.
"""

STYLESHEET = """
QMainWindow {
    background-color: #0f172a;
}

QWidget {
    font-family: "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    color: #f8fafc;
}

QTabWidget::pane {
    border: none;
    background-color: #0f172a;
    padding: 15pt;
}

QTabBar {
    background-color: transparent;
}

QTabBar::tab {
    background: transparent;
    color: #94a3b8;
    padding: 9pt 18pt;
    margin-right: 6pt;
    border-bottom: 2pt solid transparent;
}

QTabBar::tab:hover {
    color: #e2e8f0;
    background-color: rgba(255, 255, 255, 0.05);
}

QTabBar::tab:selected {
    color: #ffffff;
    border-bottom: 2pt solid #3b82f6;
    background-color: rgba(59, 130, 246, 0.1);
}

#PageTitle {
    font-size: 20pt;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8pt;
}

#StatusLabel {
    color: #94a3b8;
    font-style: italic;
    font-size: 10pt;
}

QGroupBox {
    background-color: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 9pt;
    margin-top: 15pt;
    padding: 15pt;
    font-weight: 600;
    color: #e2e8f0;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15pt;
    padding: 0 8pt;
    color: #60a5fa;
}

#StatCard, #LastScrapedCard {
    background-color: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12pt;
    padding: 15pt;
}

#StatValue {
    font-size: 26pt;
    font-weight: 800;
    color: #60a5fa;
}

#StatCaption {
    color: #94a3b8;
    font-size: 10pt;
    font-weight: 500;
}

#LastScrapedValue {
    font-size: 11pt;
    font-weight: 600;
    color: #f1f5f9;
}

QLineEdit, QTextEdit, QSpinBox {
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6pt;
    padding: 8pt 11pt;
    background-color: rgba(15, 23, 42, 0.6);
    color: #f8fafc;
}

QLineEdit:focus {
    border: 1px solid #3b82f6;
    background-color: rgba(15, 23, 42, 0.8);
}

QPushButton {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6pt;
    padding: 8pt 15pt;
    font-weight: 600;
    color: #f1f5f9;
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

QPushButton#PrimaryButton {
    background-color: #3b82f6;
    color: #ffffff;
    border: none;
}

QPushButton#PrimaryButton:hover {
    background-color: #2563eb;
}

QPushButton#DangerButton {
    background-color: rgba(239, 68, 68, 0.1);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

QPushButton#DangerButton:hover {
    background-color: rgba(239, 68, 68, 0.2);
}

QTableWidget {
    background-color: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 9pt;
    gridline-color: rgba(255, 255, 255, 0.05);
    color: #f1f5f9;
}

QTableWidget::item {
    padding: 6pt;
}

QTableWidget::item:selected {
    background-color: rgba(59, 130, 246, 0.2);
    color: #ffffff;
}

QHeaderView::section {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 8pt;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    font-weight: 700;
    text-transform: uppercase;
    font-size: 8pt;
}

QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 8pt;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 15pt;
    border-radius: 4pt;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
