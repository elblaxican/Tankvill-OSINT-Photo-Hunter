import logging
import face_recognition

logger = logging.getLogger(__name__)


class FaceEngine:
    def __init__(self, reference_image_path: str = None):
        self.reference_encoding = None

        if reference_image_path:
            try:
                image = face_recognition.load_image_file(reference_image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    self.reference_encoding = encodings[0]
                    logger.info(f"Loaded reference face: {reference_image_path}")
                else:
                    logger.warning("No face detected in reference image.")

            except Exception as e:
                logger.error(f"Failed to load reference image: {e}")

    def match(self, image_path: str):
        """Return a similarity score (0.0–1.0) or None."""
        if not self.reference_encoding:
            return None

        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                return None

            # Compute best match score
            scores = []
            for enc in encodings:
                distance = face_recognition.face_distance([self.reference_encoding], enc)[0]
                score = round(1.0 - distance, 4)
                scores.append(score)

            return max(scores)

        except Exception as e:
            logger.error(f"Face match failed for {image_path}: {e}")
            return None
