import logging
from PIL import Image
from PIL.ExifTags import TAGS

logger = logging.getLogger(__name__)


class ExifEngine:
    def __init__(self):
        pass

    def extract(self, image_path: str):
        """Extract EXIF metadata from an image."""
        try:
            image = Image.open(image_path)
            exif_data = image.getexif()

            if not exif_data:
                return {}

            readable = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                readable[tag] = value

            return readable

        except Exception as e:
            logger.error(f"EXIF extraction failed for {image_path}: {e}")
            return {}
