import cv2
import logging
from config import ConfigHandler, ConfigurationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RTSPClient:
    def __init__(self, config_path: str = None):
        """
        Initialize RTSP client

        Args:
            config_path: Path to .env file (optional)
        """
        try:
            # Load configuration
            self.config_handler = ConfigHandler(config_path)
            if not self.config_handler.validate_configuration():
                raise ConfigurationError("Configuration validation failed")

            self.rtsp_config = self.config_handler.get_rtsp_config()
            self.processing_config = self.config_handler.get_processing_config()

            # Initialize video capture
            self.cap = None

        except Exception as e:
            logger.error(f"Failed to initialize RTSP client: {str(e)}")
            raise

    def connect(self) -> bool:
        """Establish connection to RTSP stream"""
        try:
            # Create video capture with RTSP URL
            self.cap = cv2.VideoCapture(self.rtsp_config.url)

            # Configure connection parameters
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize latency

            if not self.cap.isOpened():
                raise ConnectionError("Failed to connect to RTSP stream")

            logger.info(f"Successfully connected to RTSP stream at {self.rtsp_config.url_masked}")
            return True

        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            return False

    def disconnect(self) -> None:
        """Close RTSP connection"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            logger.info("Disconnected from RTSP stream")

    def read_frame(self):
        """Read a frame from the RTSP stream"""
        if self.cap is None:
            raise ConnectionError("Not connected to RTSP stream")

        ret, frame = self.cap.read()
        if not ret:
            raise ConnectionError("Failed to read frame from stream")

        return frame


# Example usage
if __name__ == "__main__":
    try:
        # Initialize client
        client = RTSPClient()

        # Connect to stream
        if client.connect():
            # Read some frames
            for _ in range(100):  # Read 100 frames
                frame = client.read_frame()
                # Process frame here

        # Cleanup
        client.disconnect()

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")