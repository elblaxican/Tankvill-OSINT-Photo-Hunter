import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class DorkingEngine:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def search(self, target_name: str, target_handle: str = None):
        """
        Perform simple search-engine dorking to find image URLs.
        Returns a list of direct image URLs.
        """
        query = f"{target_name} profile photo"
        if target_handle:
            query += f" {target_handle}"

        url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            results = []
            for img in soup.find_all("img"):
                src = img.get("src")
                if src and src.startswith("http"):
                    results.append(src)

            logger.info(f"Dorking found {len(results)} images for query: {query}")
            return results

        except Exception as e:
            logger.error(f"Dorking search failed: {e}")
            return []
