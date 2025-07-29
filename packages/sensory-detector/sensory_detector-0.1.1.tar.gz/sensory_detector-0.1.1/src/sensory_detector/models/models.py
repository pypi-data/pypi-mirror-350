from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List

class BoundingBox(BaseModel):
    x1: float = Field(..., description="Левая граница")
    y1: float = Field(..., description="Верхняя граница")
    x2: float = Field(..., description="Правая граница")
    y2: float = Field(..., description="Нижняя граница")

class DetectedObject(BaseModel):
    index: int = Field(..., description="Уникальный индекс объекта в кадре")
    object_name: str = Field(..., description="Название объекта, распознанного YOLO ")
    confidence: float = Field(..., ge=0.0, le=1.0, description="скор модели в диапазоне от 0 до 1")
    bounding_box: BoundingBox = Field(..., description="Координаты ограничивающего прямоугольника")

class DetectionFrame(BaseModel):
    index: int = Field(..., description="Уникальный индекс кадра")
    timestamp: float = Field(..., description="Timestamp of the frame in seconds")
    detections: List[DetectedObject]

class DetectionSeries(BaseModel):
    model_name: str = Field(..., description="Модель YOLO")
    detections: List[DetectionFrame]
    
class ModelsResponse(BaseModel):
    """Response model for available models endpoint."""
    available_models: List[str] = Field(..., description="List of available model names.")
    default_model: str = Field(..., description="Name of the default model.")
    message: str = Field(..., description="Informational message.")
    
class CacheStatsResponse(BaseModel):
    """
    Схема ответа для эндпоинта /api/loaded_models (статус кэша).
    """
    model_name: str
    wrapper_class: str
    last_used: str # ISO 8601 string
    idle_seconds: float
    hits: int
    mem_bytes: int
    
class UnloadModelResponse(BaseModel):
    detail: str