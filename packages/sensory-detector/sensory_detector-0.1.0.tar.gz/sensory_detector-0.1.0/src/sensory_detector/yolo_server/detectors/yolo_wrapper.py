from ultralytics import YOLO
import cv2
import numpy as np
from typing import List
from src.sensory_detector.models.models import DetectedObject, BoundingBox, DetectionSeries, DetectionFrame
from pathlib import Path
from src.sensory_detector.yolo_server.config import config
import av
from mimetypes import guess_type            # +++
from src.sensory_detector.yolo_server.video_analizer.video_processor import process_video_sync
  
import logging
log = logging.getLogger(__name__)


class YOLOv8Wrapper:
    def __init__(self, model_name: str):
        self._model_name = model_name
        model_path = config.WEIGHTS_DIR / f"{model_name}.pt"
        log.debug(f"Initializing YOLOv8 model: {model_name}")

        if not model_path.exists():
            log.warning(f"Model weights not found at {model_path}. Attempting to download '{model_name}.pt'...")
            self.model = YOLO(f"{model_name}.pt")
            downloaded_file = Path(f"{model_name}.pt")

            if downloaded_file.exists():
                downloaded_file.rename(model_path)
                log.debug(f"Model weights successfully moved to {model_path}.")
            else:
                raise FileNotFoundError(f"Файл {downloaded_file} не найден после загрузки.")
        else:
            log.debug(f"Model weights found at {model_path}.")
        self.model = YOLO(str(model_path))
        log.debug("Model loaded successfully.")

    # file

    def model_name(self) -> str:
        return self._model_name
    
    def detect_from_file(self, file_path: str):
        """
        Лёгкий универсальный метод:
        – определяет, картинка это или видео,  
        – делегирует тяжёлую работу внешним помощникам.
        """
        mime, _ = guess_type(file_path)
        if not mime:
            raise ValueError(f"Не удаётся определить тип файла: {file_path}")
        if mime.startswith("image/"):
            img = cv2.imread(file_path)
            if img is None:
                raise IOError(f"Не удалось прочитать изображение: {file_path}")
            return self._detect(img)
        if mime.startswith("video/"):
            return process_video_sync(file_path, self)

        raise ValueError(f"Неподдерживаемый тип файла: {mime}")

    # bytes
    def detect_from_bytes(self, image_bytes: bytes) -> List[DetectedObject]:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return self._detect(img)
    
    # ndarray
    def detect_from_frame(self, frame: np.ndarray, timestamp: float = 0.0) -> List[DetectedObject]:
        """Detects objects in a video frame (numpy array)."""
        return self._detect(frame, timestamp=timestamp)


    def _detect(self, img: np.ndarray, timestamp: float = 0.0) -> List[DetectedObject]:
        log.debug("Running YOLO inference...")
        results = self.model(img, verbose=False)
        detections: List[DetectedObject] = []

        for result in results:
            boxes = result.boxes
            for i, box in enumerate(boxes):
                if len(box.cls) == 0 or len(box.conf) == 0 or len(box.xyxy) == 0:
                     log.warning(f"Skipping incomplete box data: cls={box.cls}, conf={box.conf}, xyxy={box.xyxy}")
                     continue # Пропускаем некорректные данные
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()

                bbox = BoundingBox(
                    x1=xyxy[0],
                    y1=xyxy[1],
                    x2=xyxy[2],
                    y2=xyxy[3]
                )

                detections.append(
                    DetectedObject(
                        index=i,
                        object_name=self.model.names[cls],
                        confidence=conf,
                        bounding_box=bbox
                    )
                )
              
        log.debug(f"Found {len(detections)} detections.")
        return detections
    
    
    # Добавим вспомогательный метод для обработки видеофайла
    def _process_video(self, video_path: str) -> List[DetectionFrame]:
        """
        Processes a video file frame by frame using pyAV (blocking operation).
        This method is designed to be run inside a thread pool.
        """
        log.info(f"Processing video file: {video_path}")
        detection_frames: List[DetectionFrame] = []
        container = None # Инициализация вне try
        try:
            # av.open является блокирующей операцией
            container = av.open(video_path)
            # Берем первый видео стрим
            try:
                stream = container.streams.video[0]
            except IndexError:
                log.error(f"No video stream found in {video_path}")
                raise ValueError(f"No video stream found in file: {video_path}")

            # Decode video frames - this loop is CPU bound
            for frame_index, frame in enumerate(container.decode(stream)):
                try:
                    # Convert frame to numpy array (blocking)
                    img = frame.to_ndarray(format="bgr24")
                    # Calculate timestamp
                    # frame.time * stream.time_base gives timestamp in seconds
                    # If frame.time is None or not reliable, use frame index and stream rate
                    timestamp = float(frame.time) if frame.time is not None else frame_index / stream.rate
                    # Run detection on the frame
                    detections = self.detect_from_frame(img, timestamp=timestamp)
                    # Append results for this frame
                    detection_frames.append(DetectionFrame(index=frame_index, timestamp=timestamp, detections=detections))
                    log.debug(f"Processed frame {frame_index} at {timestamp:.2f}s with {len(detections)} detections.")

                except Exception as e:
                     log.error(f"Error processing frame {frame_index}: {e}", exc_info=True)
                     # Decide how to handle frame errors: skip frame or stop? Skipping frame for now.
                     # Continue to the next frame

        except av.AVError as e:
            log.error(f"Error opening or processing video file {video_path} with pyAV: {e}", exc_info=True)
            raise IOError(f"Could not process video file {video_path}. Is it a valid video?") from e
        except Exception as e:
            log.error(f"An unexpected error occurred during video processing {video_path}: {e}", exc_info=True)
            raise RuntimeError(f"An unexpected error occurred during video processing.") from e
        finally:
            # Ensure container is closed even if errors occur
            if container:
                try:
                    container.close()
                    log.debug(f"Video container for {video_path} closed.")
                except Exception as e:
                    log.warning(f"Error closing video container for {video_path}: {e}", exc_info=True)


        log.info(f"Finished processing video file: {video_path}. Total frames processed: {len(detection_frames)}")
        return detection_frames
    
    
    def unload(self) -> None:
        """
        Освобождает VRAM / RAM.  Вызывается Cache-менеджером,
        когда модель простаивала дольше MODEL_CACHE_TIMEOUT_SEC.
        """
        log.info("Unloading YOLO model '%s' from memory …", self._model_name)
        try:
            del self.model
            #torch.cuda.empty_cache()   
        except Exception as e:
            log.warning("Error while unloading model '%s': %s",
                           self._model_name, e, exc_info=True)