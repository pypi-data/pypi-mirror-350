"""
Базовый интерфейс-протокол для любых object-detector’ов, которые
подключаются к сервису (YOLOv8, Detectron2, …).

Все методы БЛОКИРУЮЩИЕ.  Из асинхронного кода их вызываем через
`await asyncio.to_thread(detector.detect_...)`.
"""
from __future__ import annotations

from typing import Protocol, List, Union
from enum import Enum
import numpy as np

from src.sensory_detector.models.models import DetectedObject, DetectionFrame

class ModelTaskType(str, Enum):
    DETECTION = "detection"
    EMBEDDING = "embedding"

class Detector(Protocol):
    # ---------- обязательные методы / свойства ----------

    @property
    def model_name(self) -> str: ...
    def task_type(self) -> ModelTaskType: ...
    def detect_from_bytes(self, image_bytes: bytes) -> List[DetectedObject]: ...
    def detect_from_frame(self, frame: np.ndarray,
                          timestamp: float = 0.0) -> List[DetectedObject]: ...

    def detect_from_file(self, file_path: str) -> Union[
        List[DetectedObject],          # если это изображение
        List[DetectionFrame]           # если это видео
    ]: ...
    def unload(self) -> None:
        """Явное освобождение GPU-памяти и прочих ресурсов."""
        ...