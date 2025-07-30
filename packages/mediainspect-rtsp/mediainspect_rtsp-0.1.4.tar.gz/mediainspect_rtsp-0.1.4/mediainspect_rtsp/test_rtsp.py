import os
import cv2
import av
import time
import logging
#from video_processor_rtsp import VideoProcessor
from web_rtsp_processor import VideoProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv

from rtsp_client import RTSPClient


def test_rtsp_connection(rtsp_url: str, duration: int = 10):
    """
    Test RTSP connection and frame retrieval.

    Args:
        rtsp_url: RTSP stream URL
        duration: Test duration in seconds
    """
    print(f"Testing RTSP connection to: {rtsp_url}")

    try:
        # Try OpenCV first
        print("Testing with OpenCV...")
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            raise Exception("Failed to open RTSP stream with OpenCV")

        start_time = time.time()
        frames_received = 0

        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if ret:
                frames_received += 1
                if frames_received % 30 == 0:  # Print every 30 frames
                    print(f"Received {frames_received} frames...")
            else:
                print("Failed to receive frame")
                break

        fps = frames_received / duration
        print(f"OpenCV Test Results:")
        print(f"- Frames received: {frames_received}")
        print(f"- Average FPS: {fps:.2f}")

        cap.release()

    except Exception as e:
        print(f"OpenCV test failed: {str(e)}")

    try:
        # Try RTSPClient
        print("\nTesting with RTSPClient...")
        # client = RTSPClient(rtsp_url)
        # client.preview()
        # client.close()
        print("RTSPClient test successful")

    except Exception as e:
        print(f"RTSPClient test failed: {str(e)}")



def process_rtsp(url):
    cap = cv2.VideoCapture(url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Process frame here
        yield frame
    cap.release()


def process_rtsp_av(url):
    container = av.open(url)
    for frame in container.decode(video=0):
        # Process frame here
        yield frame.to_ndarray(format='rgb24')


from rtsp_client import RTSPClient

def test1():
    # Initialize client (automatically loads .env)
    client = RTSPClient()

    # Connect and read frames
    if client.connect():
        try:
            while True:
                frame = client.read_frame()
                # Process frame here
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            client.disconnect()

def test2():
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


import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test3():
    # Load environment variables
    load_dotenv()

    # Get RTSP URL from environment
    rtsp_url = os.getenv('RTSP_URL')

    if not rtsp_url:
        logger.error("RTSP_URL not found in environment variables")
        return

    logger.info(f"Using RTSP URL: {rtsp_url}")

    try:
        # Initialize processor
        processor = VideoProcessor(
            rtsp_url=rtsp_url,
            motion_threshold=25.0,
            blur_size=21,
            reconnect_attempts=3
        )

        # Run processing loop
        processor.run(display=True)

    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")


def test4():
    # Load environment variables
    load_dotenv()

    # Get RTSP URL from environment
    rtsp_url = os.getenv('RTSP_URL')

    if not rtsp_url:
        logger.error("RTSP_URL not found in environment variables")
        return

    logger.info(f"Using RTSP URL: {rtsp_url}")

    try:
        # Initialize processor
        processor = VideoProcessor(
            rtsp_url=rtsp_url,
            motion_threshold=25.0,
            blur_size=21,
            reconnect_attempts=3
        )

        # Run processing loop
        processor.run(display=True)

    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")





if __name__ == "__main__":
    # load_dotenv()
    rtsp_url=os.getenv("RTSP_URL")
    # Example RTSP URL - replace with your actual URL
    # rtsp_url = "rtsp://username:password@ip:port/stream"
    # process_rtsp_av(rtsp_url)
    # test_rtsp_connection(rtsp_url)
    # test2()
    # test3()
    test4()