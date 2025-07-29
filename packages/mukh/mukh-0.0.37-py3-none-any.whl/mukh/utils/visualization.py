import cv2
import numpy as np

from ..core.types import FaceDetection


def draw_detections(
    image: np.ndarray,
    detections: list[FaceDetection],
    color: tuple = (0, 255, 0),
    thickness: int = 2,
) -> np.ndarray:
    """
    Draw bounding boxes and landmarks on the image.

    Args:
        image: RGB image as numpy array
        detections: List of FaceDetection objects
        color: BGR color tuple for drawing
        thickness: Line thickness

    Returns:
        Image with drawn detections
    """
    img = image.copy()

    for detection in detections:
        # Draw bounding box
        bbox = detection.bbox
        cv2.rectangle(
            img,
            (int(bbox.x1), int(bbox.y1)),
            (int(bbox.x2), int(bbox.y2)),
            color,
            thickness,
        )

        # Draw landmarks if available
        if detection.landmarks is not None:
            for x, y in detection.landmarks:
                cv2.circle(img, (int(x), int(y)), 2, color, -1)

    return img
