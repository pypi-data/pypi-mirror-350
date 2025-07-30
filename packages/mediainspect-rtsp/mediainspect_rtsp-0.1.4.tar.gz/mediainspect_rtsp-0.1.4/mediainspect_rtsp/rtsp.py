from datetime import time

import cv2
import numpy as np
import av
import threading
from typing import Callable, Dict, List, Tuple, Optional
from dataclasses import dataclass
from queue import Queue


@dataclass
class VideoFrame:
    frame: np.ndarray
    timestamp: float
    frame_number: int


@dataclass
class AudioFrame:
    samples: np.ndarray
    timestamp: float
    sample_rate: int


@dataclass
class MediaBatch:
    video_frames: List[VideoFrame]
    audio_frames: List[AudioFrame]
    batch_number: int


def process_rtsp_stream(
        source_rtsp_url: str,
        target_rtsp_url: str,
        callback_processor: Callable[[MediaBatch], MediaBatch],
        batch_size: int = 30,
        reconnect_attempts: int = 3,
        buffer_size: int = 60
) -> None:
    """
    Process RTSP video stream with custom frame processing.

    Args:
        source_rtsp_url (str): Source RTSP URL with credentials (rtsp://username:password@ip:port/path)
        target_rtsp_url (str): Target RTSP server URL with credentials
        callback_processor (Callable): Function that processes batches of frames and audio
            Must accept MediaBatch and return processed MediaBatch
        batch_size (int): Number of frames to process in one batch
        reconnect_attempts (int): Number of reconnection attempts on connection loss
        buffer_size (int): Maximum number of frames to buffer

    Returns:
        None
    """

    def read_stream(input_container, frame_queue: Queue):
        try:
            for frame in input_container.decode():
                if frame_queue.qsize() < buffer_size:
                    frame_queue.put(frame)
                else:
                    # Drop oldest frame if buffer is full
                    frame_queue.get()
                    frame_queue.put(frame)
        except Exception as e:
            print(f"Error reading stream: {e}")

    def write_stream(output_container, processed_queue: Queue):
        try:
            while True:
                batch = processed_queue.get()
                if batch is None:  # Signal to stop
                    break

                for video_frame in batch.video_frames:
                    frame = av.VideoFrame.from_ndarray(video_frame.frame)
                    packet = output_container.encode(frame)
                    output_container.mux(packet)

                for audio_frame in batch.audio_frames:
                    frame = av.AudioFrame.from_ndarray(audio_frame.samples)
                    frame.sample_rate = audio_frame.sample_rate
                    packet = output_container.encode(frame)
                    output_container.mux(packet)
        except Exception as e:
            print(f"Error writing stream: {e}")

    frame_queue = Queue()
    processed_queue = Queue()

    for attempt in range(reconnect_attempts):
        try:
            # Open input stream
            input_container = av.open(source_rtsp_url, mode='r', options={
                'rtsp_transport': 'tcp',
                'stimeout': '5000000'
            })

            # Open output stream
            output_container = av.open(target_rtsp_url, mode='w', options={
                'rtsp_transport': 'tcp',
                'fflags': 'nobuffer',
                'flags': 'low_delay'
            })

            # Start reader and writer threads
            reader_thread = threading.Thread(
                target=read_stream,
                args=(input_container, frame_queue)
            )
            writer_thread = threading.Thread(
                target=write_stream,
                args=(output_container, processed_queue)
            )

            reader_thread.start()
            writer_thread.start()

            current_batch = []
            current_audio = []
            batch_number = 0

            while True:
                if not frame_queue.empty():
                    frame = frame_queue.get()

                    if isinstance(frame, av.VideoFrame):
                        numpy_frame = frame.to_ndarray(format='bgr24')
                        video_frame = VideoFrame(
                            frame=numpy_frame,
                            timestamp=frame.time,
                            frame_number=frame.index
                        )
                        current_batch.append(video_frame)

                    elif isinstance(frame, av.AudioFrame):
                        numpy_audio = frame.to_ndarray()
                        audio_frame = AudioFrame(
                            samples=numpy_audio,
                            timestamp=frame.time,
                            sample_rate=frame.sample_rate
                        )
                        current_audio.append(audio_frame)

                    if len(current_batch) >= batch_size:
                        # Process batch through callback
                        media_batch = MediaBatch(
                            video_frames=current_batch,
                            audio_frames=current_audio,
                            batch_number=batch_number
                        )

                        processed_batch = callback_processor(media_batch)
                        processed_queue.put(processed_batch)

                        current_batch = []
                        current_audio = []
                        batch_number += 1

        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt == reconnect_attempts - 1:
                print("Max reconnection attempts reached. Stopping.")
                break

            print(f"Retrying in 5 seconds...")
            time.sleep(5)
            continue

        finally:
            # Cleanup
            processed_queue.put(None)  # Signal writer to stop
            if 'reader_thread' in locals():
                reader_thread.join()
            if 'writer_thread' in locals():
                writer_thread.join()
            if 'input_container' in locals():
                input_container.close()
            if 'output_container' in locals():
                output_container.close()