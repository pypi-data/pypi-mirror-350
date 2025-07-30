import cv2
import numpy as np
from typing import List, Tuple, Dict
import logging
import os
import requests
from pathlib import Path

logger = logging.getLogger(__name__)


class ObjectDetector:
    """YOLO-based object detection"""

    def __init__(self,
                 confidence_threshold: float = 0.5,
                 nms_threshold: float = 0.4):
        """
        Initialize object detector

        Args:
            confidence_threshold: Minimum confidence for detection
            nms_threshold: Non-maximum suppression threshold
        """
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.classes = None
        self.colors = None
        self.net = None
        self.output_layers = None
        self.initialized = False

        # Model paths
        self.model_dir = Path("models")
        self.model_dir.mkdir(exist_ok=True)

        self.config_path = self.model_dir / "yolov3.cfg"
        self.weights_path = self.model_dir / "yolov3.weights"
        self.classes_path = self.model_dir / "coco.names"

        # Initialize detector
        self.initialize()

    def download_file(self, url: str, path: Path) -> bool:
        """Download file if not exists"""
        if path.exists():
            return True

        try:
            logger.info(f"Downloading {url} to {path}")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True

        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")
            return False

    def initialize(self) -> bool:
        """Initialize the detector and load model"""
        try:
            # Download model files if needed
            files = {
                "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg": self.config_path,
                "https://pjreddie.com/media/files/yolov3.weights": self.weights_path,
                "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names": self.classes_path
            }

            for url, path in files.items():
                if not self.download_file(url, path):
                    return False

            # Load class names
            with open(self.classes_path, 'r') as f:
                self.classes = [line.strip() for line in f.readlines()]

            # Generate colors for visualization
            np.random.seed(42)
            self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype='uint8')

            # Load network
            self.net = cv2.dnn.readNetFromDarknet(
                str(self.config_path),
                str(self.weights_path)
            )

            # Get output layer names
            layer_names = self.net.getLayerNames()
            self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

            self.initialized = True
            logger.info("Object detector initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize object detector: {str(e)}")
            return False

    def detect(self, frame: np.ndarray) -> Tuple[List[Dict], np.ndarray]:
        """
        Detect objects in frame

        Args:
            frame: Input frame

        Returns:
            Tuple of (detections list, annotated frame)
        """
        if not self.initialized:
            return [], frame

        height, width = frame.shape[:2]

        try:
            # Prepare image for neural network
            blob = cv2.dnn.blobFromImage(
                frame,
                1 / 255.0,
                (416, 416),
                swapRB=True,
                crop=False
            )

            # Forward pass
            self.net.setInput(blob)
            outputs = self.net.forward(self.output_layers)

            # Initialize lists for detections
            boxes = []
            confidences = []
            class_ids = []

            # Process detections
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > self.confidence_threshold:
                        # Scale coordinates to frame size
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Apply non-maximum suppression
            indices = cv2.dnn.NMSBoxes(
                boxes,
                confidences,
                self.confidence_threshold,
                self.nms_threshold
            )

            # Prepare detections list
            detections = []
            frame_annotated = frame.copy()

            for i in indices:
                if isinstance(i, (tuple, list)):
                    i = i[0]  # Handle different OpenCV versions

                box = boxes[i]
                x, y, w, h = box
                class_id = class_ids[i]
                confidence = confidences[i]

                # Add detection to list
                detection = {
                    'class': self.classes[class_id],
                    'confidence': confidence,
                    'box': box
                }
                detections.append(detection)

                # Draw detection on frame
                color = tuple(map(int, self.colors[class_id]))
                cv2.rectangle(frame_annotated, (x, y), (x + w, y + h), color, 2)

                # Add label
                label = f"{self.classes[class_id]}: {confidence:.2f}"
                cv2.putText(
                    frame_annotated,
                    label,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )

            return detections, frame_annotated

        except Exception as e:
            logger.error(f"Error in object detection: {str(e)}")
            return [], frame