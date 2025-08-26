import requests
from bs4 import BeautifulSoup
import json
import time
import os
from config.config import ARTWORK_DATA_PATH

BASE_URL = "https://www.metmuseum.org"
COLLECTION_SEARCH_URL = "https://www.metmuseum.org/art/collection/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_artwork_links(start_page=1, max_pages=1):
    links = []
    for page in range(start_page, start_page + max_pages):
        url = f"{COLLECTION_SEARCH_URL}?searchField=All&pageSize=0&sortBy=Relevance&page={page}"
        print(f"Fetching list page: {url}")
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.select("a.card__link[href*='/art/collection/search/']"):
            href = link.get("href")
            full_url = BASE_URL + href
            if full_url not in links:
                links.append(full_url)
        time.sleep(1)
    return links

def scrape_artwork_details(url):
    try:
        print(f"Scraping: {url}")
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        def safe_extract(selector):
            tag = soup.select_one(selector)
            return tag.get_text(strip=True) if tag else None

        return {
            "title": safe_extract("h2.card__title"),
            "artist": safe_extract("div.card__artist a"),
            "date": safe_extract("div.object-details__date"),
            "medium": safe_extract("div.object-details__medium"),
            "dimensions": safe_extract("div.object-details__dimensions"),
            "description": safe_extract("div.rte__text"),
            "url": url
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main(output_path=ARTWORK_DATA_PATH, max_pages=1):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    artwork_links = get_artwork_links(max_pages=max_pages)
    print(f"Found {len(artwork_links)} artwork links. Scraping details...")
    with open(output_path, "w", encoding="utf-8") as f:
        for url in artwork_links:
            data = scrape_artwork_details(url)
            if data and data["title"]:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
            time.sleep(1)
    print(f"Scraping complete. Data saved to {output_path}")

if __name__ == "__main__":
    main(max_pages=2)  # Scrape 2 pages (~40–60 artworks)