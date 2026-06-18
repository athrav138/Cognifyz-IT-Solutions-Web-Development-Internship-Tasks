"""
scraper/engine.py

Responsible for sending the HTTP request to a target website and
returning the raw response (or a structured error) for the parser
module to work with. Keeping this separate from parser.py means the
network layer can be swapped or mocked independently of HTML parsing.
"""

import time
from dataclasses import dataclass
from typing import Optional

import requests


class ScraperError(Exception):
    """Raised for any scraping failure with a user-friendly message."""
    def __init__(self, message: str, code: str = "GENERIC"):
        super().__init__(message)
        self.message = message
        self.code = code


@dataclass
class FetchResult:
    url: str
    html: str
    status_code: int
    response_time: float
    content_type: str
    server: str
    page_size: int


DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = "Mozilla/5.0 (WebScraperPro/1.0)"


def validate_url(url: str) -> str:
    """
    Basic URL validation/normalization. Adds https:// if no scheme given.
    Raises ScraperError if the URL still looks invalid.
    """
    url = (url or "").strip()
    if not url:
        raise ScraperError("Please enter a valid website address.", code="INVALID_URL")

    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url

    # Extremely lightweight sanity check: must contain a dot after the scheme
    # and no internal whitespace.
    stripped = url.split("://", 1)[-1]
    if " " in url or "." not in stripped:
        raise ScraperError("Please enter a valid website address.", code="INVALID_URL")

    return url


def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT, user_agent: str = DEFAULT_USER_AGENT) -> FetchResult:
    """
    Send a GET request to `url` and return a FetchResult.
    Raises ScraperError with a descriptive code/message on any failure,
    so the GUI layer can show the right message without knowing about
    the `requests` exception hierarchy.
    """
    url = validate_url(url)
    headers = {"User-Agent": user_agent}

    start = time.time()
    try:
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
    except requests.exceptions.ConnectionError:
        raise ScraperError("No internet connection or the server could not be reached.", code="CONNECTION_ERROR")
    except requests.exceptions.Timeout:
        raise ScraperError(f"The request timed out after {timeout} seconds.", code="TIMEOUT")
    except requests.exceptions.MissingSchema:
        raise ScraperError("Please enter a valid website address.", code="INVALID_URL")
    except requests.exceptions.RequestException as exc:
        raise ScraperError(f"Request failed: {exc}", code="REQUEST_ERROR")

    elapsed = time.time() - start

    if response.status_code == 403:
        raise ScraperError("403 Forbidden. Try changing the User-Agent in Settings.", code="FORBIDDEN")
    if response.status_code == 404:
        raise ScraperError("404 Not Found. The page does not exist.", code="NOT_FOUND")
    if response.status_code >= 400:
        raise ScraperError(f"Server returned error status {response.status_code}.", code="HTTP_ERROR")

    return FetchResult(
        url=str(response.url),
        html=response.text,
        status_code=response.status_code,
        response_time=round(elapsed, 3),
        content_type=response.headers.get("Content-Type", ""),
        server=response.headers.get("Server", "Unknown"),
        page_size=len(response.content),
    )
