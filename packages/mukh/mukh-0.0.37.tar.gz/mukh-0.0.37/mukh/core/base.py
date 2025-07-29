from abc import ABC, abstractmethod
from typing import List

import numpy as np

from ..core.types import FaceDetection


class BaseDetector(ABC):
    """Abstract base class for all face detectors."""

    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold

    @abstractmethod
    def detect(self, image: np.ndarray) -> List[FaceDetection]:
        """
        Detect faces in the given image.

        Args:
            image: numpy array of shape (H, W, 3) in RGB format

        Returns:
            List of FaceDetection objects
        """
        pass

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Optional preprocessing step."""
        return image
