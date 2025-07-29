from dataclasses import dataclass
from typing import List, Optional

import numpy as np


@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float = 1.0

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1


@dataclass
class FaceDetection:
    bbox: BoundingBox
    landmarks: Optional[np.ndarray] = None
