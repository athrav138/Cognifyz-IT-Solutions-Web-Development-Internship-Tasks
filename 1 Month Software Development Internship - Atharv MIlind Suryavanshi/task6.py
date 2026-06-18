import requests
from bs4 import BeautifulSoup


def print_heading(title):
    print("\n" + "-" * 40)
    print(title.center(40))
    print("-" * 40)


class WebScraper:

    @staticmethod
    def scrape(url):
        try:
            # Browser header to avoid 403 errors
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, "html.parser")

            # Website Title
            print_heading("WEBSITE TITLE")

            if soup.title and soup.title.string:
                print(soup.title.string.strip())
            else:
                print("No title found")

            # Headings
            print_heading("HEADINGS")

            headings = soup.find_all(["h1", "h2", "h3"])

            if headings:
                for i, heading in enumerate(headings[:20], start=1):
                    text = heading.get_text(strip=True)

                    if text:
                        print(f"{i}. {text}")
            else:
                print("No headings found")

            # Links
            print_heading("LINKS")

            links = soup.find_all("a")

            count = 0

            for link in links:
                href = link.get("href")

                if href:
                    count += 1
                    print(f"{count}. {href}")

                if count == 20:
                    break

            if count == 0:
                print("No links found")

            print_heading("SCRAPING COMPLETED")

        except requests.exceptions.HTTPError as e:
            print_heading("HTTP ERROR")
            print(e)

        except requests.exceptions.ConnectionError:
            print_heading("CONNECTION ERROR")
            print("Unable to connect to the website.")

        except requests.exceptions.Timeout:
            print_heading("TIMEOUT ERROR")
            print("The website took too long to respond.")

        except requests.exceptions.InvalidURL:
            print_heading("INVALID URL")
            print("Please enter a correct website address.")

        except requests.exceptions.RequestException as e:
            print_heading("REQUEST ERROR")
            print(e)


def main():
    print_heading("WEB SCRAPER")

    while True:
        print("1. Scrape Website")
        print("2. Exit")
        print("-" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            print("-" * 40)

            url = input("Enter website URL: ").strip()

            if not url:
                print_heading("ERROR")
                print("URL cannot be empty")
                continue

            # Add HTTPS automatically
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            WebScraper.scrape(url)

        elif choice == "2":
            print_heading("EXITING WEB SCRAPER")
            break

        else:
            print_heading("INVALID INPUT")
            print("Please enter 1 or 2")


if __name__ == "__main__":
    main()