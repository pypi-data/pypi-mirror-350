"""
Лёгкая обёртка вокруг FrameReader + Detector.
"""
import logging
import asyncio
from typing import List, TYPE_CHECKING
from src.sensory_detector.models.models import DetectionFrame
from src.sensory_detector.yolo_server.video_analizer.frame_reader import FrameReader, FrameReadError
from src.sensory_detector.yolo_server.detectors.detector_interface import Detector
if TYPE_CHECKING:
    from src.sensory_detector.yolo_server.cache_manager import ModelCache

_logger = logging.getLogger(__name__)

ACTIVITY_UPDATE_INTERVAL_FRAMES = 30

def process_video_sync(video_path: str,
                       detector: Detector,
                       model_cache: 'ModelCache', # Accept model_cache instance
                       event_loop: asyncio.AbstractEventLoop # Accept the event loop
                      ) -> List[DetectionFrame]:
    """
    Блокирующая обработка видео-файла кадр за кадром.
    Вызывается из thread-pool’а.
    """
    _logger.info(f"Processing video file sync: {video_path} with model {detector.model_name()}")
    frames: List[DetectionFrame] = []
    last_activity_update_frame = -1 # Track last frame when activity was updated

    try:
        with FrameReader(video_path) as reader:
            for idx, np_frame, ts in reader.read_frames():
                # --- Периодически обновляем активность модели ---
                if idx - last_activity_update_frame >= ACTIVITY_UPDATE_INTERVAL_FRAMES:
                    try:
                        # Вызываем async метод кэша из синхронного потока
                        asyncio.run_coroutine_threadsafe(
                            model_cache._async_update_activity(detector.model_name()),
                            event_loop
                        )
                        last_activity_update_frame = idx
                        # _logger.debug(f"Sent activity update for model '{detector.model_name()}' at frame {idx}") # Слишком много логов
                    except Exception as update_e:
                        _logger.warning(f"Failed to send activity update for model '{detector.model_name()}' at frame {idx}: {update_e}", exc_info=True)
                        # Не критично, если пропустили один пинг, продолжаем обработку

                # --- Выполняем детекцию на кадре ---
                try:
                    detections = detector.detect_from_frame(np_frame, timestamp=ts)
                    frames.append(DetectionFrame(index=idx,
                                                 timestamp=ts,
                                                 detections=detections))
                    # _logger.debug("Detected frame %s", idx) # Может быть слишком много логов
                except Exception as detection_e:
                    _logger.error("Detection error on frame %s: %s", idx, detection_e, exc_info=True)
                    # Решаем, что делать при ошибке детекции кадра - пропустить или остановить? Пропускаем.
                    # Продолжаем цикл

    except FrameReadError as fr_e:
        _logger.error(f"Error reading video file {video_path}: {fr_e}", exc_info=True)
        # Перевыбросим ошибку, т.к. не удалось прочитать видео
        raise RuntimeError(f"Could not process video file: {fr_e}") from fr_e
    except Exception as e:
        _logger.error(f"An unexpected error occurred during video processing for {video_path}: {e}", exc_info=True)
        # Перевыбросим любую другую ошибку
        raise RuntimeError(f"An unexpected error occurred during video processing: {e}") from e

    _logger.info(f"Finished processing video file sync: {video_path}. Processed {len(frames)} frames.")
    return frames