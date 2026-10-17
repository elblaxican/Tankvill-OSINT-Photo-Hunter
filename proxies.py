import logging
import random

logger = logging.getLogger(__name__)


class ProxyManager:
    def __init__(self):
        # You can expand this list later or load from config.yaml
        self.proxies = [
            # Example format:
            # "http://username:password@proxyserver:port"
            # "http://123.45.67.89:8080"
        ]

    def get_proxy(self):
        """Return a random proxy or None if no proxies are configured."""
        if not self.proxies:
            return None

        proxy = random.choice(self.proxies)
        logger.info(f"Using proxy: {proxy}")

        return {
            "http": proxy,
            "https": proxy
        }
