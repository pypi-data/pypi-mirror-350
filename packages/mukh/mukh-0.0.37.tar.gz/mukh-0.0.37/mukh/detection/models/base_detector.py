"""Base class defining the interface for face detection implementations.

This module provides the abstract base class that all face detector implementations
must inherit from, ensuring a consistent interface across different models.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

import cv2
import numpy as np

from ...core.types import FaceDetection


class BaseFaceDetector(ABC):
    """Abstract base class for face detector implementations.

    All face detector implementations must inherit from this class and implement
    the required abstract methods.

    Attributes:
        confidence_threshold: Float threshold (0-1) for detection confidence.
    """

    def __init__(self, confidence_threshold: float = 0.5):
        """Initializes the face detector.

        Args:
            confidence_threshold: Minimum confidence threshold for detections.
                Defaults to 0.5.
        """
        self.confidence_threshold = confidence_threshold

    def _load_image(self, image_path: str) -> np.ndarray:
        """Loads an image from disk in BGR format.

        Args:
            image_path: Path to the image file.

        Returns:
            np.ndarray: The loaded image in BGR format.

        Raises:
            ValueError: If the image cannot be loaded from the given path.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from path: {image_path}")
        return image

    @abstractmethod
    def detect(self, image_path: str) -> List[FaceDetection]:
        """Detects faces in the given image.

        Args:
            image_path: Path to the input image.

        Returns:
            List of FaceDetection objects containing detected faces.
        """
        pass

    @abstractmethod
    def detect_with_landmarks(
        self, image_path: str
    ) -> Tuple[List[FaceDetection], np.ndarray]:
        """Detects faces and returns annotated image with landmarks.

        Args:
            image_path: Path to the input image.

        Returns:
            tuple: (List[FaceDetection], numpy.ndarray)
                - List of FaceDetection objects containing detected faces
                - Annotated image with detections drawn
        """
        pass
