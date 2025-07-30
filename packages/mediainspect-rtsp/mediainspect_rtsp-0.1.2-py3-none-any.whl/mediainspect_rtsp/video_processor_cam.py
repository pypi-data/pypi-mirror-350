import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import time
from collections import deque


@dataclass
class ProcessingStats:
    fps: float
    frame_count: int
    dropped_frames: int
    processing_time: float
    resolution: Tuple[int, int]
    motion_detected: bool
    objects_detected: Dict[str, int]


class VideoProcessor:
    def __init__(self,
                 motion_threshold: float = 25.0,
                 blur_size: int = 21,
                 min_object_size: int = 1000,
                 max_object_size: int = 100000,
                 history_size: int = 30):
        """
        Initialize video processor with configuration parameters.

        Args:
            motion_threshold: Threshold for motion detection
            blur_size: Gaussian blur kernel size
            min_object_size: Minimum object size in pixels
            max_object_size: Maximum object size in pixels
            history_size: Number of frames to keep in history
        """
        self.motion_threshold = motion_threshold
        self.blur_size = blur_size
        self.min_object_size = min_object_size
        self.max_object_size = max_object_size

        # Initialize background subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history_size,
            varThreshold=16,
            detectShadows=True
        )

        # Initialize object detector
        self.object_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Initialize processing stats
        self.stats = ProcessingStats(
            fps=0.0,
            frame_count=0,
            dropped_frames=0,
            processing_time=0.0,
            resolution=(0, 0),
            motion_detected=False,
            objects_detected={}
        )

        # Initialize frame history
        self.frame_history = deque(maxlen=history_size)
        self.last_frame_time = time.time()

    def detect_motion(self, frame: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Detect motion in frame using background subtraction.

        Args:
            frame: Input frame

        Returns:
            Tuple of (motion detected boolean, motion mask)
        """
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(frame, (self.blur_size, self.blur_size), 0)

        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(blurred)

        # Remove shadows
        _, fg_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)

        # Apply morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

        # Calculate the amount of motion
        motion_pixels = np.sum(fg_mask == 255)
        motion_percentage = (motion_pixels / fg_mask.size) * 100

        return motion_percentage > self.motion_threshold, fg_mask

    def detect_objects(self, frame: np.ndarray) -> List[Tuple[str, float, Tuple[int, int, int, int]]]:
        """
        Detect objects in frame using cascade classifier.

        Args:
            frame: Input frame

        Returns:
            List of (object_type, confidence, bounding_box)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect objects
        objects = self.object_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        results = []
        for (x, y, w, h) in objects:
            # Calculate simple confidence based on size
            size = w * h
            if self.min_object_size <= size <= self.max_object_size:
                confidence = min((size - self.min_object_size) /
                                 (self.max_object_size - self.min_object_size), 1.0)
                results.append(("face", confidence, (x, y, w, h)))

        return results

    def draw_annotations(self,
                         frame: np.ndarray,
                         motion_mask: np.ndarray,
                         objects: List[Tuple[str, float, Tuple[int, int, int, int]]]) -> np.ndarray:
        """
        Draw detection results on frame.

        Args:
            frame: Input frame
            motion_mask: Motion detection mask
            objects: List of detected objects

        Returns:
            Annotated frame
        """
        # Draw motion overlay
        motion_overlay = cv2.addWeighted(
            frame,
            1,
            cv2.cvtColor(motion_mask, cv2.COLOR_GRAY2BGR),
            0.3,
            0
        )

        # Draw object boxes
        for obj_type, confidence, (x, y, w, h) in objects:
            cv2.rectangle(motion_overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label = f"{obj_type}: {confidence:.2f}"
            cv2.putText(
                motion_overlay,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        # Draw stats
        stats_text = [
            f"FPS: {self.stats.fps:.1f}",
            f"Frames: {self.stats.frame_count}",
            f"Dropped: {self.stats.dropped_frames}",
            f"Motion: {'Yes' if self.stats.motion_detected else 'No'}"
        ]

        for i, text in enumerate(stats_text):
            cv2.putText(
                motion_overlay,
                text,
                (10, 30 + i * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

        return motion_overlay

    def update_stats(self, motion_detected: bool, objects: List[Tuple[str, float, Tuple[int, int, int, int]]]):
        """Update processing statistics."""
        current_time = time.time()
        self.stats.fps = 1.0 / (current_time - self.last_frame_time)
        self.last_frame_time = current_time

        self.stats.frame_count += 1
        self.stats.motion_detected = motion_detected

        # Update object counts
        self.stats.objects_detected = {}
        for obj_type, _, _ in objects:
            self.stats.objects_detected[obj_type] = \
                self.stats.objects_detected.get(obj_type, 0) + 1

    def your_processing_function(self, frame: np.ndarray) -> Tuple[np.ndarray, ProcessingStats]:
        """
        Main processing function to be used with RTSP stream.

        Args:
            frame: Input frame from RTSP stream

        Returns:
            Tuple of (processed frame, processing statistics)
        """
        if frame is None:
            self.stats.dropped_frames += 1
            return None, self.stats

        # Update frame resolution
        self.stats.resolution = frame.shape[:2]

        # Start processing timer
        start_time = time.time()

        # Detect motion
        motion_detected, motion_mask = self.detect_motion(frame)

        # Detect objects if motion is detected
        objects = []
        if motion_detected:
            objects = self.detect_objects(frame)

        # Draw annotations
        processed_frame = self.draw_annotations(frame, motion_mask, objects)

        # Add to frame history
        self.frame_history.append(processed_frame)

        # Update processing stats
        self.stats.processing_time = time.time() - start_time
        self.update_stats(motion_detected, objects)

        return processed_frame, self.stats


# Example usage:
def example_usage():
    # Initialize processor
    processor = VideoProcessor(
        motion_threshold=25.0,
        blur_size=21,
        min_object_size=1000,
        max_object_size=100000
    )

    # Open video capture
    cap = cv2.VideoCapture(0)  # Use 0 for webcam or RTSP URL

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame
        processed_frame, stats = processor.your_processing_function(frame)

        if processed_frame is not None:
            # Display results
            cv2.imshow('Processed Frame', processed_frame)

            # Print stats
            print(f"FPS: {stats.fps:.1f}, Motion: {stats.motion_detected}, "
                  f"Objects: {stats.objects_detected}")

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    example_usage()
    
    
