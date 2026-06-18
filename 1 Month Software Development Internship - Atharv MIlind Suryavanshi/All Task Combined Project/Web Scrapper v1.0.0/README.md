# WebScraper Pro

A modern desktop application for scraping website information, featuring a sleek, dark-themed UI. Built with **Python** and **PyQt6**.

## Features

- **Sleek Dark Interface**: High-quality UI inspired by modern web aesthetics.
- **Scraping Engine**: Extract titles, descriptions, headings, links, and images.
- **Local Database**: Every successful scrape is automatically saved to a local SQLite database.
- **Dashboard**: View aggregate stats (websites scraped, total links/images) and recent activity.
- **History**: Search, browse, inspect, or delete past scrapes.
- **Customizable**: Adjust request timeout, User-Agent, and parsing limits in Settings.
- **Exports**: Save scrape results as TXT, JSON, or CSV reports.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The first run creates `webscraper.db` and `settings.json` in the project root automatically.

## Deployment

To create a standalone executable for Windows:

```bash
# Install development dependencies
pip install pyinstaller

# Run the build script
python build.py
```

The executable will be generated in the `dist/` folder.

## Project Structure

- `main.py`: Entry point and Qt event loop.
- `gui/`: PyQt6 screen definitions and logic.
- `scraper/`: Core scraping engine and HTML parser.
- `database/`: SQLite schema, models, and query functions.
- `storage/`: Report exporters (TXT, JSON, CSV).
- `assets/themes/style.py`: The application's modern dark QSS stylesheet.
- `utils/config.py`: Settings persistence logic.

## Technical Details

- **Backend**: Python 3.x, Requests, BeautifulSoup4 (lxml).
- **Frontend**: PyQt6 with custom QSS styling.
- **Database**: SQLite3.
