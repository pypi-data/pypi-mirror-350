from dataclasses import dataclass
from typing import Tuple, Dict

@dataclass
class ProcessingStats:
    fps: float
    frame_count: int
    dropped_frames: int
    processing_time: float
    resolution: Tuple[int, int]
    motion_detected: bool
    objects_detected: Dict[str, int]
