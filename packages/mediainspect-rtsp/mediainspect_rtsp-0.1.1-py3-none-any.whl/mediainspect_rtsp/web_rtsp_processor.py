import cv2
import numpy as np
import time
import logging
from typing import Tuple, Optional, Any, Dict
from datetime import datetime
import os
from dotenv import load_dotenv
from flask import Flask, Response, render_template
import threading
from queue import Queue
import json
from object_detector import ObjectDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy types"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

def serialize_stats(stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize statistics to JSON-compatible format

    Args:
        stats: Dictionary of statistics

    Returns:
        Dictionary with JSON-serializable values
    """
    serializable_stats = {}

    for key, value in stats.items():
        if isinstance(value, tuple):
            value = list(value)
        elif isinstance(value, np.ndarray):
            value = value.tolist()
        elif isinstance(value, (np.integer, np.floating, np.bool_)):
            value = value.item()
        serializable_stats[key] = value

    return serializable_stats



class FrameRateLimiter:
    """Class to handle frame rate limiting"""

    def __init__(self, target_fps: float):
        """
        Initialize frame rate limiter

        Args:
            target_fps: Target frames per second
        """
        self.target_fps = target_fps
        self.frame_interval = 1.0 / target_fps
        self.last_frame_time = 0
        self.frame_count = 0
        self.start_time = time.time()

    def should_process_frame(self) -> bool:
        """
        Check if we should process this frame based on target FPS

        Returns:
            bool: True if frame should be processed
        """
        current_time = time.time()
        elapsed = current_time - self.last_frame_time

        if elapsed >= self.frame_interval:
            self.last_frame_time = current_time
            self.frame_count += 1
            return True
        return False

    def get_actual_fps(self) -> float:
        """
        Calculate actual FPS

        Returns:
            float: Current actual FPS
        """
        elapsed = time.time() - self.start_time
        return self.frame_count / elapsed if elapsed > 0 else 0

    def reset(self):
        """Reset the limiter"""
        self.frame_count = 0
        self.start_time = time.time()
        self.last_frame_time = 0



# Initialize Flask app
app = Flask(__name__)

# Global queues for thread communication
frame_queue = Queue(maxsize=10)
stats_queue = Queue(maxsize=10)

class VideoProcessor:
    def __init__(self,
                 rtsp_url: Optional[str] = None,
                 target_fps: float = 3.0,
                 motion_threshold: float = 25.0,
                 blur_size: int = 21,
                 min_object_size: int = 1000,
                 max_object_size: int = 100000,
                 reconnect_attempts: int = 3,
                 reconnect_delay: int = 5,
                 enable_object_detection: bool = True,
                 confidence_threshold: float = 0.5):
        """Initialize VideoProcessor with object detection"""

        # Initialize object detector
        self.enable_object_detection = enable_object_detection
        if self.enable_object_detection:
            self.object_detector = ObjectDetector(
                confidence_threshold=confidence_threshold
            )
        self.rtsp_url = rtsp_url
        self.target_fps = target_fps
        self.motion_threshold = motion_threshold
        self.blur_size = blur_size
        self.min_object_size = min_object_size
        self.max_object_size = max_object_size
        self.reconnect_attempts = reconnect_attempts
        self.reconnect_delay = reconnect_delay

        self.last_frame_time = time.time()
        self.frame_count = 0
        self.start_time = time.time()

        # Initialize frame rate limiter
        self.frame_limiter = FrameRateLimiter(target_fps)

        self.cap = None
        self.is_connected = False
        self.is_running = False

        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=100,
            varThreshold=16,
            detectShadows=True
        )

        # Initialize statistics
        self.stats = {
            'processed_frames': 0,
            'skipped_frames': 0,
            'total_frames': 0,
            'actual_fps': 0.0,
            'target_fps': float(target_fps),
            'motion_detected': False,
            'motion_percentage': 0.0,
            'frame_size': (0, 0),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Add object detection stats
        self.stats.update({
            'objects_detected': [],
            'detection_count': 0,
            'object_detection_enabled': enable_object_detection
        })

        if self.rtsp_url:
            self.connect()

    def stop(self):
        """Stop the processing loop"""
        self.is_running = False

    def connect(self) -> bool:
        """Connect to RTSP stream with robust error handling"""
        if not self.rtsp_url:
            logger.error("No RTSP URL provided")
            return False

        for attempt in range(self.reconnect_attempts):
            try:
                logger.info(f"Connecting to RTSP stream (attempt {attempt + 1}/{self.reconnect_attempts})")

                # Create capture object with RTSP-specific settings
                self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)

                # Configure stream
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                if not self.cap.isOpened():
                    raise Exception("Failed to open RTSP stream")

                # Read test frame
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    raise Exception("Failed to read from stream")

                # Reset timing variables
                self.is_connected = True
                self.last_frame_time = time.time()
                self.frame_count = 0
                self.start_time = time.time()

                # Get stream information
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                stream_fps = self.cap.get(cv2.CAP_PROP_FPS)

                logger.info(
                    f"Successfully connected to RTSP stream "
                    f"(Target FPS: {self.target_fps}, "
                    f"Resolution: {width}x{height}, "
                    f"Stream FPS: {stream_fps})"
                )

                # Update initial statistics
                self.stats.update({
                    'frame_size': (height, width),
                    'stream_fps': float(stream_fps),
                    'processed_frames': 0,
                    'skipped_frames': 0,
                    'total_frames': 0,
                    'actual_fps': 0.0
                })

                return True

            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if self.cap:
                    self.cap.release()
                    self.cap = None

                if attempt < self.reconnect_attempts - 1:
                    logger.info(f"Waiting {self.reconnect_delay} seconds before next attempt...")
                    time.sleep(self.reconnect_delay)

        logger.error("All connection attempts failed")
        return False

    def run(self):
        """Main processing loop"""
        if not self.is_connected and not self.connect():
            logger.error("Not connected to stream")
            return

        self.is_running = True
        frames_processed = 0
        frames_skipped = 0

        try:
            while self.is_running:
                self.stats['total_frames'] += 1

                # Check if we should process this frame
                if not self.frame_limiter.should_process_frame():
                    frames_skipped += 1
                    self.stats['skipped_frames'] = frames_skipped

                    # Read and discard frame to keep buffer clear
                    self.cap.grab()
                    continue

                # Read frame
                ret, frame = self.cap.read()

                if not ret or frame is None:
                    logger.warning("Failed to read frame, attempting reconnection...")
                    if not self.connect():
                        break
                    continue

                # Process frame
                processed_frame, stats = self.process_frame(frame)

                if processed_frame is not None:
                    frames_processed += 1
                    self.stats['processed_frames'] = frames_processed
                    self.stats['actual_fps'] = self.frame_limiter.get_actual_fps()

                    # Update stats with frame rate information
                    stats.update(self.stats)

                    # Convert frame to JPEG
                    _, buffer = cv2.imencode('.jpg', processed_frame)
                    frame_bytes = buffer.tobytes()

                    # Update queues
                    if not frame_queue.full():
                        frame_queue.put(frame_bytes)
                    if not stats_queue.full():
                        stats_queue.put(stats)

                # Log performance stats periodically
                if frames_processed % 30 == 0:
                    logger.info(
                        f"Performance: Processed={frames_processed}, "
                        f"Skipped={frames_skipped}, "
                        f"Actual FPS={self.stats['actual_fps']:.1f}, "
                        f"Target FPS={self.stats['target_fps']}"
                    )

        except Exception as e:
            logger.error(f"Error in processing loop: {str(e)}")
        finally:
            self.is_running = False
            self.disconnect()


    def should_process_frame(self) -> bool:
        """Check if frame should be processed based on target FPS"""
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        target_interval = 1.0 / self.target_fps

        if elapsed >= target_interval:
            self.last_frame_time = current_time
            self.frame_count += 1
            return True
        return False

    def get_actual_fps(self) -> float:
        """Calculate actual FPS"""
        elapsed = time.time() - self.start_time
        return self.frame_count / elapsed if elapsed > 0 else 0



    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Process a single frame with object detection"""
        if frame is None:
            return None, self.stats

        # Update frame size
        self.stats['frame_size'] = frame.shape[:2]

        # Create copy for processing
        processed = frame.copy()

        try:
            # Motion detection (existing code)
            blurred = cv2.GaussianBlur(frame, (self.blur_size, self.blur_size), 0)
            fg_mask = self.bg_subtractor.apply(blurred)
            _, fg_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
            motion_pixels = np.sum(fg_mask == 255)
            motion_percentage = float((motion_pixels / fg_mask.size) * 100)

            # Object detection
            if self.enable_object_detection:
                detections, processed = self.object_detector.detect(processed)

                # Update statistics
                self.stats.update({
                    'objects_detected': [
                        {
                            'class': d['class'],
                            'confidence': float(d['confidence'])
                        } for d in detections
                    ],
                    'detection_count': len(detections)
                })

            # Motion overlay if significant motion detected
            if motion_percentage > self.motion_threshold:
                motion_overlay = cv2.addWeighted(
                    processed,
                    1,
                    cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR),
                    0.3,
                    0
                )
                processed = motion_overlay

            # Update all statistics
            self.stats.update({
                'motion_detected': bool(motion_percentage > self.motion_threshold),
                'motion_percentage': motion_percentage,
                'actual_fps': float(self.get_actual_fps()),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Add overlay text
            font = cv2.FONT_HERSHEY_SIMPLEX
            y_pos = 30

            def add_text(text: str):
                nonlocal y_pos
                cv2.putText(processed, text, (10, y_pos), font, 1, (0, 255, 255), 2)
                y_pos += 40

            add_text(f"FPS: {self.stats['actual_fps']:.1f}/{self.target_fps}")
            add_text(f"Motion: {self.stats['motion_percentage']:.1f}%")

            if self.enable_object_detection:
                detected_objects = [f"{d['class']} ({d['confidence']:.2f})"
                                    for d in self.stats['objects_detected']]
                if detected_objects:
                    add_text(f"Objects: {', '.join(detected_objects)}")

            add_text(self.stats['timestamp'])

            return processed, serialize_stats(self.stats)

        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return None, self.stats



    def disconnect(self):
        """Disconnect from RTSP stream"""
        if self.cap:
            self.cap.release()
            self.cap = None
        self.is_connected = False
        logger.info("Disconnected from RTSP stream")


    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, dict]:
        """Process a single frame"""
        if frame is None:
            return None, {}

        # Create copy for processing
        processed = frame.copy()

        # Motion detection
        blurred = cv2.GaussianBlur(frame, (self.blur_size, self.blur_size), 0)
        fg_mask = self.bg_subtractor.apply(blurred)

        # Remove shadows
        _, fg_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)

        # Calculate motion
        motion_pixels = np.sum(fg_mask == 255)
        motion_percentage = (motion_pixels / fg_mask.size) * 100

        # Draw motion overlay if significant motion detected
        if motion_percentage > self.motion_threshold:
            motion_overlay = cv2.addWeighted(
                processed,
                1,
                cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR),
                0.3,
                0
            )
            processed = motion_overlay

        # Add timestamp and stats
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Add text with background for better visibility
        def put_text_with_background(img, text, pos, font=font, scale=1, thickness=2):
            text_size = cv2.getTextSize(text, font, scale, thickness)[0]
            text_box_pos = (pos[0], pos[1] + 5)
            cv2.rectangle(img,
                          (pos[0] - 5, pos[1] - text_size[1] - 5),
                          (pos[0] + text_size[0] + 5, pos[1] + 5),
                          (0, 0, 0),
                          -1)
            cv2.putText(img, text, text_box_pos, font, scale, (255, 255, 255), thickness)

        # Add information overlay
        put_text_with_background(processed, timestamp, (10, 30))
        put_text_with_background(processed,
                                 f"Motion: {motion_percentage:.1f}%",
                                 (10, 70))

        # Collect statistics
        stats = {
            'timestamp': timestamp,
            'motion_detected': motion_percentage > self.motion_threshold,
            'motion_percentage': motion_percentage,
            'frame_size': frame.shape,
        }

        return processed, stats

    def run(self):
        """Main processing loop"""
        if not self.is_connected and not self.connect():
            logger.error("Not connected to stream")
            return

        self.is_running = True
        self.start_time = time.time()
        self.frame_count = 0

        try:
            while self.is_running:
                # Check if we should process this frame
                if not self.should_process_frame():
                    # Skip frame but update statistics
                    self.stats['skipped_frames'] += 1
                    self.cap.grab()  # Discard frame
                    continue

                ret, frame = self.cap.read()

                if not ret or frame is None:
                    logger.warning("Failed to read frame, attempting reconnection...")
                    if not self.connect():
                        break
                    continue

                # Update frame counts
                self.stats['total_frames'] += 1
                self.stats['processed_frames'] += 1

                # Process frame
                processed_frame, stats = self.process_frame(frame)

                if processed_frame is not None:
                    # Convert frame to JPEG
                    _, buffer = cv2.imencode('.jpg', processed_frame)
                    frame_bytes = buffer.tobytes()

                    # Update queues
                    if not frame_queue.full():
                        frame_queue.put(frame_bytes)
                    if not stats_queue.full():
                        stats_queue.put(stats)

        except Exception as e:
            logger.error(f"Error in processing loop: {str(e)}")
        finally:
            self.is_running = False
            self.disconnect()

def gen_frames():
    """Generator for video streaming"""
    while True:
        if not frame_queue.empty():
            frame_bytes = frame_queue.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            time.sleep(0.01)


def gen_stats():
    """Generator for statistics streaming"""
    while True:
        if not stats_queue.empty():
            stats = stats_queue.get()
            try:
                # Use custom encoder for NumPy types
                json_stats = json.dumps(stats, cls=NumpyEncoder)
                yield f"data: {json_stats}\n\n"
            except Exception as e:
                logger.error(f"Error serializing stats: {str(e)}")
        else:
            time.sleep(0.01)


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stats_feed')
def stats_feed():
    """Statistics streaming route"""
    return Response(gen_stats(),
                    mimetype='text/event-stream')