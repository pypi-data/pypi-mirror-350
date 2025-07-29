"""BlazeFace face detection model implementation.

This module implements the BlazeFace face detection model from MediaPipe.
Adapted from: https://github.com/hollance/BlazeFace-PyTorch
Original implementation by M.I. Hollemans.

The model is optimized for mobile devices and provides both bounding box
detection and 6 facial landmarks.
"""

from typing import List, Tuple

import cv2
import numpy as np
import torch
from pkg_resources import resource_filename

from ....core.types import BoundingBox, FaceDetection
from ..base_detector import BaseFaceDetector
from .blazeface_torch import BlazeFace


class BlazeFaceDetector(BaseFaceDetector):
    """BlazeFace face detector implementation.

    A lightweight face detector that provides both bounding boxes and facial
    landmarks. Optimized for mobile devices.

    Attributes:
        device: PyTorch device (CPU/CUDA) for model execution
        net: BlazeFace neural network model
        confidence_threshold: Minimum confidence for valid detections
    """

    def __init__(
        self,
        weights_path: str = None,
        anchors_path: str = None,
        confidence_threshold: float = 0.75,
    ):
        """Initializes the BlazeFace detector.

        Args:
            weights_path: Optional custom path to model weights file
            anchors_path: Optional custom path to anchor boxes file
            confidence_threshold: Minimum confidence threshold for detections
        """
        super().__init__(confidence_threshold)

        # Use default paths from package if not provided
        if weights_path is None:
            weights_path = resource_filename(
                "mukh", "detection/models/blazeface/blazeface.pth"
            )
        if anchors_path is None:
            anchors_path = resource_filename(
                "mukh", "detection/models/blazeface/anchors.npy"
            )

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.net = BlazeFace().to(self.device)
        self.net.load_weights(weights_path)
        self.net.load_anchors(anchors_path)

    def detect(self, image_path: str) -> List[FaceDetection]:
        """Detects faces in the given image.

        The image is resized to 128x128 pixels for inference and the results
        are scaled back to the original image size.

        Args:
            image_path: Path to the input image.

        Returns:
            List[FaceDetection]: List of detected faces, each containing:
                - bbox: BoundingBox with coordinates and confidence
                - landmarks: Array of 6 facial keypoints
        """
        # Load image from path
        image = self._load_image(image_path)

        # Get original dimensions
        orig_h, orig_w = image.shape[:2]

        # Resize to 128x128
        image_resized = cv2.resize(image, (128, 128))

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

        # Get detections
        detections = self.net.predict_on_image(image_rgb)

        # Convert to FaceDetection objects
        faces = []
        for detection in detections:
            # Convert normalized coordinates back to original image size
            x1 = float(detection[1]) * orig_w  # xmin
            y1 = float(detection[0]) * orig_h  # ymin
            x2 = float(detection[3]) * orig_w  # xmax
            y2 = float(detection[2]) * orig_h  # ymax

            bbox = BoundingBox(
                x1=x1, y1=y1, x2=x2, y2=y2, confidence=float(detection[16])
            )

            # Extract landmarks and scale back to original size
            landmarks = []
            for i in range(6):
                x = float(detection[4 + i * 2]) * orig_w
                y = float(detection[4 + i * 2 + 1]) * orig_h
                landmarks.append([x, y])

            faces.append(FaceDetection(bbox=bbox, landmarks=np.array(landmarks)))

        return faces

    def detect_with_landmarks(
        self, image_path: str
    ) -> Tuple[List[FaceDetection], np.ndarray]:
        """Detects faces and returns annotated image with landmarks.

        Args:
            image_path: Path to the input image.

        Returns:
            tuple: Contains:
                - List[FaceDetection]: List of detected faces
                - np.ndarray: Copy of input image with detections drawn
        """
        # Load image and detect faces
        image = self._load_image(image_path)
        faces = self.detect(image_path)

        # Draw detections on image copy
        annotated_image = self._draw_detections(image, faces)
        return faces, annotated_image

    def _draw_detections(
        self, image: np.ndarray, faces: List[FaceDetection]
    ) -> np.ndarray:
        """Draws detection results on the image.

        Args:
            image: Input image as numpy array
            faces: List of detected faces

        Returns:
            np.ndarray: Copy of input image with bounding boxes and landmarks drawn
        """
        image_copy = image.copy()
        for face in faces:
            bbox = face.bbox
            # Draw bounding box
            cv2.rectangle(
                image_copy,
                (int(bbox.x1), int(bbox.y1)),
                (int(bbox.x2), int(bbox.y2)),
                (0, 255, 0),
                2,
            )

            # Draw landmarks
            if face.landmarks is not None:
                for x, y in face.landmarks:
                    cv2.circle(image_copy, (int(x), int(y)), 2, (0, 255, 0), 2)

        return image_copy
