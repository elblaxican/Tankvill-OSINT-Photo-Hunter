import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from core.face import FaceEngine
from core.exif import ExifEngine
from core.dorking import DorkingEngine
from core.proxies import ProxyManager
from core.utils import download_image

# Each module will be imported dynamically
from modules.github import GitHubModule
from modules.instagram import InstagramModule
from modules.reddit import RedditModule
from modules.tiktok import TikTokModule
from modules.youtube import YouTubeModule
from modules.linkedin import LinkedInModule

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class PhotoHunter:
    def __init__(self, target_name: str, target_handle: str = None, reference_image: str = None):
        self.target_name = target_name
        self.target_handle = target_handle
        self.reference_image = reference_image

        # Engines
        self.face_engine = FaceEngine(reference_image)
        self.exif_engine = ExifEngine()
        self.dorking_engine = DorkingEngine()
        self.proxy_manager = ProxyManager()

        # Modules (photo-only)
        self.modules = [
            GitHubModule,
            InstagramModule,
            RedditModule,
            TikTokModule,
            YouTubeModule,
            LinkedInModule,
        ]

        # Output structure
        self.results: Dict[str, Dict] = {}

        # Ensure download directory exists
        os.makedirs("assets/downloads", exist_ok=True)

    def run_module(self, module_class):
        """Run a single OSINT module."""
        try:
            module = module_class(
                target_name=self.target_name,
                target_handle=self.target_handle,
                proxy_manager=self.proxy_manager
            )

            output = module.run()

            # Process photos: download + EXIF + face match
            processed_photos = []
            for photo in output.get("photos", []):
                local_path = download_image(photo["url"], module.platform_name)

                exif = self.exif_engine.extract(local_path)
                face_score = self.face_engine.match(local_path)

                processed_photos.append({
                    "url": photo["url"],
                    "local_path": local_path,
                    "exif": exif,
                    "face_match": face_score
                })

            return module.platform_name, {
                "photos": processed_photos,
                "metadata": {},
                "errors": output.get("errors", [])
            }

        except Exception as e:
            logger.error(f"Module {module_class.__name__} failed: {e}")
            return module_class.__name__, {
                "photos": [],
                "metadata": {},
                "errors": [str(e)]
            }

    def run_all(self):
        """Run all modules in parallel."""
        logger.info("Starting parallel OSINT scan...")

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = {
                executor.submit(self.run_module, module): module.__name__
                for module in self.modules
            }

            for future in as_completed(futures):
                platform_name, result = future.result()
                self.results[platform_name] = result

        # Add search-engine dorking
        dork_urls = self.dorking_engine.search(self.target_name, self.target_handle)
        dork_photos = []

        for url in dork_urls:
            local_path = download_image(url, "dorking")
            exif = self.exif_engine.extract(local_path)
            face_score = self.face_engine.match(local_path)

            dork_photos.append({
                "url": url,
                "local_path": local_path,
                "exif": exif,
                "face_match": face_score
            })

        self.results["Dorking"] = {
            "photos": dork_photos,
            "metadata": {},
            "errors": []
        }

        return self.results

    def save_results(self, path="osint_results.json"):
        """Save final structured JSON output."""
        with open(path, "w") as f:
            json.dump(self.results, f, indent=4)
        logger.info(f"Results saved to {path}")
