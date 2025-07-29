"""
Лёгкая обёртка вокруг FrameReader + Detector.
"""
import logging
from typing import List
from src.sensory_detector.models.models import DetectionFrame
from src.sensory_detector.yolo_server.video_analizer.frame_reader import FrameReader, FrameReadError
from src.sensory_detector.yolo_server.detectors.detector_interface import Detector

_logger = logging.getLogger(__name__)

def process_video_sync(video_path: str, detector: Detector) -> List[DetectionFrame]:
    """
    Блокирующая обработка видео-файла кадр за кадром.
    Вызывается из thread-pool’а.
    """
    frames: List[DetectionFrame] = []
    with FrameReader(video_path) as reader:
        for idx, np_frame, ts in reader.read_frames():
            try:
                detections = detector.detect_from_frame(np_frame, timestamp=ts)
                frames.append(DetectionFrame(index=idx,
                                             timestamp=ts,
                                             detections=detections))
            except Exception as e:
                _logger.error("Detection error on frame %s: %s", idx, e, exc_info=True)
    return frames