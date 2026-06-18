"""
gui/dashboard.py

Landing screen showing high-level counters: total websites scraped,
total links found, total images found, and the last scraped website.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from database import queries


class StatCard(QFrame):
    def __init__(self, label: str):
        super().__init__()
        self.setObjectName("StatCard")
        layout = QVBoxLayout(self)
        self.value_label = QLabel("0")
        self.value_label.setObjectName("StatValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        caption = QLabel(label)
        caption.setObjectName("StatCaption")
        caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
        layout.addWidget(caption)

    def set_value(self, value):
        self.value_label.setText(str(value))


class DashboardPage(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header_row = QHBoxLayout()
        title = QLabel("Web Scraper Pro")
        title.setObjectName("PageTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        header_row.addWidget(refresh_btn)
        layout.addLayout(header_row)

        cards_row = QHBoxLayout()
        self.websites_card = StatCard("Total Websites Scraped")
        self.links_card = StatCard("Total Links Found")
        self.images_card = StatCard("Total Images Found")
        cards_row.addWidget(self.websites_card)
        cards_row.addWidget(self.links_card)
        cards_row.addWidget(self.images_card)
        layout.addLayout(cards_row)

        last_group = QFrame()
        last_group.setObjectName("LastScrapedCard")
        last_layout = QVBoxLayout(last_group)
        caption = QLabel("Last Scraped Website")
        caption.setObjectName("StatCaption")
        self.last_value = QLabel("(none yet)")
        self.last_value.setObjectName("LastScrapedValue")
        last_layout.addWidget(caption)
        last_layout.addWidget(self.last_value)
        layout.addWidget(last_group)

        # Analytics Chart
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.figure.patch.set_facecolor('#0f172a')
        self.ax.set_facecolor('#1e293b')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, stretch=1)

        layout.addStretch()

    def refresh(self):
        stats = queries.get_dashboard_stats(self.conn)
        self.websites_card.set_value(stats["total_websites"])
        self.links_card.set_value(stats["total_links"])
        self.images_card.set_value(stats["total_images"])
        
        # Update Chart
        self.ax.clear()
        labels = ['Links', 'Images']
        values = [stats["total_links"], stats["total_images"]]
        
        bars = self.ax.bar(labels, values, color=['#3b82f6', '#8b5cf6'])
        self.ax.tick_params(colors='#94a3b8', labelsize=9)
        self.ax.spines['bottom'].set_color('#334155')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#334155')
        self.ax.set_title("Content Distribution", color='#f1f5f9', fontsize=11, fontweight='bold')
        
        self.canvas.draw()

        if stats["last_url"]:
            self.last_value.setText(f"{stats['last_url']}\n{stats['last_date']}")
        else:
            self.last_value.setText("(none yet)")
