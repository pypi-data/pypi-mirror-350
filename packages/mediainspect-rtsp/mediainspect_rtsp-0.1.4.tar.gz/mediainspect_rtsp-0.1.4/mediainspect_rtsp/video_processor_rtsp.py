import cv2
import numpy as np
import time
import logging
from typing import Tuple, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoProcessor:
    def __init__(self,
                 rtsp_url: Optional[str] = None,
                 motion_threshold: float = 25.0,
                 blur_size: int = 21,
                 min_object_size: int = 1000,
                 max_object_size: int = 100000,
                 reconnect_attempts: int = 3,
                 reconnect_delay: int = 5):
        """
        Initialize video processor for RTSP stream
        """
        self.rtsp_url = rtsp_url
        self.motion_threshold = motion_threshold
        self.blur_size = blur_size
        self.min_object_size = min_object_size
        self.max_object_size = max_object_size
        self.reconnect_attempts = reconnect_attempts
        self.reconnect_delay = reconnect_delay

        # Initialize capture object
        self.cap = None
        self.is_connected = False

        # Initialize background subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=100,
            varThreshold=16,
            detectShadows=True
        )

        if self.rtsp_url:
            self.connect()

    def connect(self, rtsp_url: Optional[str] = None) -> bool:
        """Connect to RTSP stream with robust error handling"""
        if rtsp_url:
            self.rtsp_url = rtsp_url

        if not self.rtsp_url:
            logger.error("No RTSP URL provided")
            return False

        for attempt in range(self.reconnect_attempts):
            try:
                logger.info(f"Connecting to RTSP stream (attempt {attempt + 1}/{self.reconnect_attempts})")

                # Create capture object with RTSP-specific settings
                self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)

                # Configure RTSP stream settings
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                # Set RTSP transport protocol - using FFmpeg options
                success = self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
                if not success:
                    logger.warning("Failed to set H264 codec")

                # Use FFmpeg command-line options for RTSP transport
                command_line = (
                    f"ffmpeg -rtsp_transport tcp "  # Force TCP
                    f"-buffer_size 10240000 "  # Larger buffer for stability
                    f"-stimeout 5000000 "  # Socket timeout (microseconds)
                    f"-i {self.rtsp_url} "  # Input stream
                    f"-vsync 0 "  # No frame dropping
                    f"-copyts "  # Copy timestamps
                    f"-y"  # Overwrite output
                )

                os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = command_line

                if not self.cap.isOpened():
                    raise Exception("Failed to open RTSP stream")

                # Read test frame
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    raise Exception("Failed to read from stream")

                self.is_connected = True
                logger.info("Successfully connected to RTSP stream")

                # Log stream information
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                logger.info(f"Stream info - Resolution: {width}x{height}, FPS: {fps}")

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

    def run(self, display: bool = True):
        """Main processing loop"""
        if not self.is_connected and not self.connect():
            logger.error("Not connected to stream")
            return

        try:
            frame_count = 0
            start_time = time.time()

            while True:
                ret, frame = self.cap.read()

                if not ret or frame is None:
                    logger.warning("Failed to read frame, attempting reconnection...")
                    if not self.connect():
                        break
                    continue

                frame_count += 1

                # Calculate FPS
                elapsed_time = time.time() - start_time
                current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0

                # Process frame
                processed_frame, stats = self.process_frame(frame)

                if processed_frame is not None and display:
                    # Add FPS to display
                    cv2.putText(processed_frame,
                                f"FPS: {current_fps:.1f}",
                                (10, 110),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 255, 255),
                                2)

                    cv2.imshow('Processed RTSP Stream', processed_frame)

                    # Print stats
                    if stats.get('motion_detected'):
                        logger.info(f"Motion detected: {stats['motion_percentage']:.2f}%")

                # Break on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            logger.info("Processing interrupted by user")
        except Exception as e:
            logger.error(f"Error in processing loop: {str(e)}")
        finally:
            self.disconnect()
            cv2.destroyAllWindows()


def main():
    # Load environment variables
    load_dotenv()

    # Get RTSP URL from environment or use default
    rtsp_url = os.getenv('RTSP_URL')

    if not rtsp_url:
        logger.error("RTSP_URL not found in environment variables")
        return

    # Initialize processor
    processor = VideoProcessor(
        rtsp_url=rtsp_url,
        motion_threshold=25.0,
        blur_size=21,
        reconnect_attempts=3
    )

    # Run processing loop
    processor.run()


if __name__ == "__main__":
    main()