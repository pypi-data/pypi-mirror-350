"""
Ultra-Light face detection model implementation.

This module implements the Ultra-Light-Fast-Generic-Face-Detector-1MB.
Adapted from: https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB

Original implementation by Linzaer
"""

import os
from typing import List, Tuple

import cv2
import numpy as np
import torch
from pkg_resources import resource_filename

from ....core.types import BoundingBox, FaceDetection
from ..base_detector import BaseFaceDetector
from .vision.ssd.config.fd_config import define_img_size
from .vision.ssd.mb_tiny_fd import create_mb_tiny_fd, create_mb_tiny_fd_predictor
from .vision.ssd.mb_tiny_RFB_fd import (
    create_Mb_Tiny_RFB_fd,
    create_Mb_Tiny_RFB_fd_predictor,
)


class UltralightDetector(BaseFaceDetector):
    """Ultra-Light face detector implementation.

    A 1MB size face detector optimized for edge devices. Provides bounding
    box detection without landmarks.

    Attributes:
        device: PyTorch device (CPU/CUDA) for model execution
        input_size: Input resolution for the model
        net: Neural network model
        predictor: Detection predictor instance
        confidence_threshold: Minimum confidence for valid detections
    """

    def __init__(
        self,
        net_type: str = "RFB",
        input_size: int = 320,
        confidence_threshold: float = 0.9,
        candidate_size: int = 1500,
        weights_path: str = None,
        labels_path: str = None,
    ):
        """Initializes the Ultra-Light face detector.

        Args:
            net_type: Network architecture type ("RFB" or "slim")
            input_size: Input image size for the model
            confidence_threshold: Minimum confidence threshold for detections
            candidate_size: Maximum number of candidate detections
            weights_path: Optional custom path to model weights file
            labels_path: Optional custom path to class labels file
        """
        super().__init__(confidence_threshold)

        # Use default paths from package if not provided
        if weights_path is None:
            weights_path = resource_filename(
                "mukh", "detection/models/ultralight/pretrained/version-RFB-320.pth"
            )
        if labels_path is None:
            labels_path = resource_filename(
                "mukh", "detection/models/ultralight/voc-model-labels.txt"
            )

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.input_size = input_size

        # Define image size before importing predictor
        define_img_size(input_size)

        # Load class names
        self.class_names = [name.strip() for name in open(labels_path).readlines()]

        # Initialize network based on type
        if net_type == "slim":
            self.net = create_mb_tiny_fd(
                len(self.class_names), is_test=True, device=self.device
            )
            self.predictor = create_mb_tiny_fd_predictor(
                self.net, candidate_size=candidate_size, device=self.device
            )
        elif net_type == "RFB":
            self.net = create_Mb_Tiny_RFB_fd(
                len(self.class_names), is_test=True, device=self.device
            )
            self.predictor = create_Mb_Tiny_RFB_fd_predictor(
                self.net, candidate_size=candidate_size, device=self.device
            )
        else:
            raise ValueError("net_type must be either 'slim' or 'RFB'")

        # Load weights
        self.net.load(weights_path)
        self.candidate_size = candidate_size

    def detect(self, image_path: str) -> List[FaceDetection]:
        """Detects faces in the given image using Ultra-Light model.

        The image is resized to self.input_size for inference and results
        are scaled back to original image size.

        Args:
            image_path: Path to the input image.

        Returns:
            List[FaceDetection]: List of detected faces, each containing:
                - bbox: BoundingBox with coordinates and confidence
                - landmarks: None (Ultralight doesn't provide landmarks)
        """
        # Load image from path
        image = self._load_image(image_path)
        orig_height, orig_width = image.shape[:2]

        # Resize image to input size
        resized_image = cv2.resize(image, (self.input_size, self.input_size))

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # Get detections
        boxes, labels, probs = self.predictor.predict(
            image_rgb, self.candidate_size / 2, self.confidence_threshold
        )

        # Scale factors for converting back to original size
        width_scale = orig_width / self.input_size
        height_scale = orig_height / self.input_size

        # Convert to FaceDetection objects
        faces = []
        for i in range(boxes.size(0)):
            box = boxes[i, :].int().tolist()
            # Scale bounding box back to original image size
            bbox = BoundingBox(
                x1=float(box[0] * width_scale),
                y1=float(box[1] * height_scale),
                x2=float(box[2] * width_scale),
                y2=float(box[3] * height_scale),
                confidence=float(probs[i]),
            )
            # Ultralight doesn't provide landmarks, so we pass None
            faces.append(FaceDetection(bbox=bbox, landmarks=None))

        return faces

    def detect_with_landmarks(
        self, image_path: str
    ) -> Tuple[List[FaceDetection], np.ndarray]:
        """Detects faces and returns annotated image.

        Note: This model does not provide facial landmarks.

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

        Draws bounding boxes and confidence scores in red color.

        Args:
            image: Input image as numpy array
            faces: List of detected faces

        Returns:
            np.ndarray: Copy of input image with bounding boxes and confidence scores drawn
        """
        image_copy = image.copy()
        for face in faces:
            bbox = face.bbox
            # Draw bounding box
            cv2.rectangle(
                image_copy,
                (int(bbox.x1), int(bbox.y1)),
                (int(bbox.x2), int(bbox.y2)),
                (0, 0, 255),  # Red color (BGR)
                2,
            )

            # Add confidence score
            label = f"{bbox.confidence:.2f}"
            cv2.putText(
                image_copy,
                label,
                (int(bbox.x1), int(bbox.y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

        return image_copy
