"""Face detection module providing a unified interface for multiple detection models.

This module provides a factory class for creating face detectors with different
underlying implementations. It supports multiple detection models through a consistent
interface.

Example:
    Basic usage with default settings:

    >>> from mukh.detection import FaceDetector
    >>> detector = FaceDetector.create("blazeface")
    >>> faces = detector.detect("image.jpg")

    List available models:

    >>> FaceDetector.list_available_models()
    ['blazeface', 'mediapipe', 'ultralight']
"""

from typing import List, Literal

from .models.base_detector import BaseFaceDetector
from .models.blazeface import BlazeFaceDetector
from .models.mediapipe import MediaPipeFaceDetector
from .models.ultralight import UltralightDetector

DetectorType = Literal["blazeface", "mediapipe", "ultralight"]


class FaceDetector:
    """Factory class for creating face detection model instances.

    This class provides a unified interface to create and use different face detection
    models through a consistent API.
    """

    @staticmethod
    def create(model: DetectorType) -> BaseFaceDetector:
        """Creates a face detector instance of the specified type.

        Args:
            model: The type of detector to create. Must be one of: "blazeface",
                "mediapipe", or "ultralight".

        Returns:
            A BaseFaceDetector instance of the requested type.

        Raises:
            ValueError: If the specified model type is not supported.
        """
        detectors = {
            "blazeface": BlazeFaceDetector,
            "mediapipe": MediaPipeFaceDetector,
            "ultralight": UltralightDetector,
        }

        if model not in detectors:
            raise ValueError(
                f"Unknown detector model: {model}. "
                f"Available models: {list(detectors.keys())}"
            )

        return detectors[model]()

    @staticmethod
    def list_available_models() -> List[str]:
        """Returns a list of available face detection model names.

        Returns:
            List of strings containing supported model names.
        """
        return ["blazeface", "mediapipe", "ultralight"]
