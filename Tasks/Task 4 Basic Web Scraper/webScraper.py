import requests
from bs4 import BeautifulSoup

class webpageScrapping:
    def __init__(self):
        self.url = "https://quotes.toscrape.com/"
        self.html = None
        self.soup = None

    def requestingPage(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.html = response.text
            print("Page downloaded successfully!\n")
        except Exception as e:
            print(f"Error downloading page: {e}")

    def showData(self):
        if self.html is None:
            print("No HTML data found. Please run requestingPage() first!")
            return

        self.soup = BeautifulSoup(self.html, "html.parser")

        # Extract quotes from span tags (class="text")
        quotes = self.soup.find_all("span", class_="text")

        print("Top Quotes:\n")
        for i, q in enumerate(quotes[:10], start=1):   # first 10
            print(f"{i}. {q.get_text(strip=True)}")


def main():
    scraper = webpageScrapping()
    scraper.requestingPage()
    scraper.showData()

if __name__ == "__main__":
    main()
