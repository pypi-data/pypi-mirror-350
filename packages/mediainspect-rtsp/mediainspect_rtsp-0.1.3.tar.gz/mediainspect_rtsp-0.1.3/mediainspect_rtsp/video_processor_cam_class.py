import cv2
import numpy as np
from collections import deque
import time
from .processing_stats import ProcessingStats

class VideoProcessor:
    def __init__(self,
                 motion_threshold: float = 25.0,
                 blur_size: int = 21,
                 min_object_size: int = 1000,
                 max_object_size: int = 100000,
                 history_size: int = 30):
        self.motion_threshold = motion_threshold
        self.blur_size = blur_size
        self.min_object_size = min_object_size
        self.max_object_size = max_object_size
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history_size,
            varThreshold=16,
            detectShadows=True
        )
        self.object_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.stats = ProcessingStats(
            fps=0.0,
            frame_count=0,
            dropped_frames=0,
            processing_time=0.0,
            resolution=(0, 0),
            motion_detected=False,
            objects_detected={}
        )
        self.frame_history = deque(maxlen=history_size)
        self.last_frame_time = time.time()
    # ... (rest of VideoProcessor methods)
