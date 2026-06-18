"""
gui/settings_page.py

Lets the user configure request timeout, user agent string, the
maximum links/images stored per scrape, and the default export folder.
Settings are persisted to settings.json via utils/config.py.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QSpinBox,
    QPushButton, QHBoxLayout, QFileDialog, QMessageBox
)

from utils.config import load_settings, save_settings


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.load_current()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Settings")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)

        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(1, 120)
        self.timeout_input.setSuffix(" seconds")
        form.addRow("Request timeout:", self.timeout_input)

        self.user_agent_input = QLineEdit()
        form.addRow("User Agent:", self.user_agent_input)

        self.max_links_input = QSpinBox()
        self.max_links_input.setRange(0, 100000)
        self.max_links_input.setSpecialValueText("No limit")
        form.addRow("Maximum links:", self.max_links_input)

        self.max_images_input = QSpinBox()
        self.max_images_input.setRange(0, 100000)
        self.max_images_input.setSpecialValueText("No limit")
        form.addRow("Maximum images:", self.max_images_input)

        folder_row = QHBoxLayout()
        self.export_folder_input = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_folder)
        folder_row.addWidget(self.export_folder_input)
        folder_row.addWidget(browse_btn)
        form.addRow("Default export folder:", folder_row)

        layout.addLayout(form)

        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)
        layout.addStretch()

    def load_current(self):
        settings = load_settings()
        self.timeout_input.setValue(settings.get("timeout", 10))
        self.user_agent_input.setText(settings.get("user_agent", ""))
        self.max_links_input.setValue(settings.get("max_links", 100))
        self.max_images_input.setValue(settings.get("max_images", 50))
        self.export_folder_input.setText(settings.get("export_folder", ""))

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Export Folder", self.export_folder_input.text())
        if folder:
            self.export_folder_input.setText(folder)

    def save(self):
        settings = {
            "timeout": self.timeout_input.value(),
            "user_agent": self.user_agent_input.text().strip() or "Mozilla/5.0 (WebScraperPro/1.0)",
            "max_links": self.max_links_input.value(),
            "max_images": self.max_images_input.value(),
            "export_folder": self.export_folder_input.text().strip() or ".",
        }
        try:
            save_settings(settings)
            QMessageBox.information(self, "Saved", "Settings saved successfully.")
        except OSError as e:
            QMessageBox.critical(self, "Save Failed", f"Unable to save settings.\n\n{e}")
