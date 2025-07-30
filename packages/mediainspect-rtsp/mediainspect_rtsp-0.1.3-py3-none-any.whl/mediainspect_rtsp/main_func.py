import os
import threading
from dotenv import load_dotenv
from .video_processor_rtsp_class import VideoProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    load_dotenv()
    rtsp_url = os.getenv('RTSP_URL')
    target_fps = float(os.getenv('TARGET_FPS', '3.0'))
    if not rtsp_url:
        logger.error("RTSP_URL not found in environment variables")
        return
    processor = VideoProcessor(
        rtsp_url=rtsp_url,
        motion_threshold=25.0,
        blur_size=21,
        reconnect_attempts=3
    )
    processor.run()

if __name__ == "__main__":
    main()
