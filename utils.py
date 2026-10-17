import os
import logging
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def sanitize_filename(url: str) -> str:
    """Create a safe filename from a URL."""
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)

    if not name:
        name = "image.jpg"

    return name.replace("/", "_").replace("\\", "_")


def download_image(url: str, platform: str) -> str:
    """Download an image and save it to assets/downloads/<platform>/."""
    try:
        folder = os.path.join("assets", "downloads", platform)
        os.makedirs(folder, exist_ok=True)

        filename = sanitize_filename(url)
        path = os.path.join(folder, filename)

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(path, "wb") as f:
            f.write(response.content)

        logger.info(f"Downloaded image: {path}")
        return path

    except Exception as e:
        logger.error(f"Failed to download image from {url}: {e}")
        return None
