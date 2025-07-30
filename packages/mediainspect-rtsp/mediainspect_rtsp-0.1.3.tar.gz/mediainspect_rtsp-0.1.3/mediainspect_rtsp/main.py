from web_rtsp_processor import app, VideoProcessor
import threading
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Load environment variables
    load_dotenv()

    # Get configuration from environment
    rtsp_url = os.getenv('RTSP_URL')
    target_fps = float(os.getenv('TARGET_FPS', '3.0'))

    if not rtsp_url:
        logger.error("RTSP_URL not found in environment variables")
        return

    # Initialize processor
    processor = VideoProcessor(
        rtsp_url=rtsp_url,
        target_fps=target_fps,
        motion_threshold=25.0,
        blur_size=21,
        reconnect_attempts=3
    )

    # Start processing in a separate thread
    processor_thread = threading.Thread(target=processor.run)
    processor_thread.daemon = True
    processor_thread.start()

    try:
        # Run Flask app
        app.run(host='0.0.0.0', port=5002, debug=False)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        processor.stop()
        processor_thread.join()


if __name__ == "__main__":
    main()