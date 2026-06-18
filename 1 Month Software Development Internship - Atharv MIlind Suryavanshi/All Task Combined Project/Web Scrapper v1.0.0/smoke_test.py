
import sys
import os

# Mock PyQt6 for headless testing if needed, but here we just test non-GUI parts
try:
    from database.connection import init_db, get_connection
    from scraper.engine import fetch_url, validate_url
    from scraper.parser import parse_html, FetchResult
    from database import queries
    print("Core modules imported successfully.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

def test_db():
    db_path = "test_webscraper.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    try:
        init_db(db_path)
        conn = get_connection(db_path)
        stats = queries.get_dashboard_stats(conn)
        assert stats["total_websites"] == 0
        print("Database initialized and stats retrieved.")
        conn.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)

def test_parser():
    html = "<html><head><title>Test Title</title></head><body><h1>Heading 1</h1><a href='/link1'>Link 1</a><img src='img1.jpg' alt='Alt 1'></body></html>"
    fetch_result = FetchResult(
        url="https://example.com",
        html=html,
        status_code=200,
        response_time=0.1,
        content_type="text/html",
        server="TestServer",
        page_size=len(html)
    )
    site = parse_html(fetch_result)
    assert site.title == "Test Title"
    assert len(site.headings) == 1
    assert site.headings[0].text == "Heading 1"
    assert len(site.links) == 1
    assert site.links[0] == "https://example.com/link1"
    assert len(site.images) == 1
    assert site.images[0].image_url == "https://example.com/img1.jpg"
    print("Parser test passed.")

if __name__ == "__main__":
    try:
        test_db()
        test_parser()
        print("Smoke test completed successfully!")
    except Exception as e:
        print(f"Smoke test failed: {e}")
        sys.exit(1)
