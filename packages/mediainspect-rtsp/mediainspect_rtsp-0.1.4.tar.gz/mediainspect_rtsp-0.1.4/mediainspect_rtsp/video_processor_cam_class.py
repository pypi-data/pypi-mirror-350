import cv2
import numpy as np
from collections import deque
import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

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
        self.history_size = history_size

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

        # Initialize frame history and timing
        self.frame_history = deque(maxlen=history_size)
        self.last_frame_time = time.time()
        self.last_stats_update = time.time()
        self.frame_times = deque(maxlen=30)  # For FPS calculation

    def detect_motion(self, frame: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Detect motion in frame using background subtraction.

        Args:
            frame: Input frame (BGR format)

        Returns:
            Tuple of (motion_detected, motion_mask)
        """
        # Convert to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (self.blur_size, self.blur_size), 0)
        
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(blurled)
        
        # Threshold the foreground mask
        _, thresh = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY)
        
        # Apply morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Check for significant motion
        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > self.min_object_size:
                motion_detected = True
                break
                
        return motion_detected, thresh

    def detect_objects(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect objects in the frame.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of detected objects with their properties
        """
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect objects
        objects = self.object_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Convert to list of dicts
        detections = []
        for (x, y, w, h) in objects:
            detections.append({
                'class': 'face',
                'confidence': 1.0,  # Cascade classifiers don't provide confidence
                'box': (x, y, w, h),
                'center': (x + w//2, y + h//2)
            })
            
        return detections

    def process_frame(self, frame: np.ndarray) -> dict:
        """
        Process a single frame.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary containing processing results
        """
        start_time = time.time()
        
        # Update frame history
        self.frame_history.append(frame.copy())
        
        # Update resolution if needed
        if self.stats.resolution != frame.shape[:2]:
            self.stats.resolution = frame.shape[:2]
        
        # Detect motion
        motion_detected, motion_mask = self.detect_motion(frame)
        self.stats.motion_detected = motion_detected
        
        # Detect objects
        objects = self.detect_objects(frame)
        
        # Update statistics
        self._update_stats(len(objects) > 0 or motion_detected, len(objects))
        
        # Calculate processing time
        self.stats.processing_time = (time.time() - start_time) * 1000  # ms
        
        return {
            'frame': frame,
            'motion_detected': motion_detected,
            'motion_mask': motion_mask,
            'objects': objects,
            'stats': self.stats
        }

    def _update_stats(self, motion_detected: bool, num_objects: int):
        """Update processing statistics."""
        current_time = time.time()
        
        # Update FPS calculation
        self.frame_times.append(current_time)
        if len(self.frame_times) > 1:
            time_diff = self.frame_times[-1] - self.frame_times[0]
            self.stats.fps = (len(self.frame_times) - 1) / time_diff if time_diff > 0 else 0
        
        # Update frame count and motion state
        self.stats.frame_count += 1
        self.stats.motion_detected = motion_detected
        
        # Update object counts (simplified example)
        self.stats.objects_detected = {'face': num_objects}
        
        # Update last frame time
        self.last_frame_time = current_time

    def get_stats(self) -> ProcessingStats:
        """Get current processing statistics."""
        return self.stats

    def reset(self):
        """Reset the processor state."""
        self.stats = ProcessingStats(
            fps=0.0,
            frame_count=0,
            dropped_frames=0,
            processing_time=0.0,
            resolution=(0, 0),
            motion_detected=False,
            objects_detected={}
        )
        self.frame_history.clear()
        self.frame_times.clear()
        self.last_frame_time = time.time()
        self.last_stats_update = time.time()
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=self.history_size,
            varThreshold=16,
            detectShadows=True
        )
