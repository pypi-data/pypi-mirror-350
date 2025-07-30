import rtsp

import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import time
from collections import deque

    
    
def my_processor(media_batch: MediaBatch) -> MediaBatch:
    # Process video frames
    for video_frame in media_batch.video_frames:
        # Your video processing logic here
        # E.g., apply filters, object detection, etc.
        processed_frame = your_processing_function(video_frame.frame)
        video_frame.frame = processed_frame

    # Process audio frames if needed
    for audio_frame in media_batch.audio_frames:
        # Your audio processing logic here
        pass

    return media_batch


# Use the function
process_rtsp_stream(
    source_rtsp_url="rtsp://user:pass@192.168.1.100:554/stream",
    target_rtsp_url="rtsp://user:pass@192.168.1.200:554/stream",
    callback_processor=my_processor
)