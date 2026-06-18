"""
utils/config.py

Loads and saves user-configurable settings (request timeout, user agent,
max links/images to store, default export folder) to a small JSON file
next to the application, so they persist between runs.
"""

import json
import os
from utils.paths import get_base_dir

APP_DIR = get_base_dir()
CONFIG_PATH = os.path.join(APP_DIR, "settings.json")
DEFAULT_EXPORT_DIR = os.path.join(APP_DIR, "reports")

DEFAULTS = {
    "timeout": 10,
    "user_agent": "Mozilla/5.0 (WebScraperPro/1.0)",
    "max_links": 100,
    "max_images": 50,
    "export_folder": DEFAULT_EXPORT_DIR,
}


def load_settings() -> dict:
    """Return saved settings merged over the defaults."""
    settings = dict(DEFAULTS)
    if os.path.isfile(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
            settings.update(saved)
        except (json.JSONDecodeError, OSError):
            pass
    os.makedirs(settings["export_folder"], exist_ok=True)
    return settings


def save_settings(settings: dict) -> None:
    """Persist `settings` to disk as JSON."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
