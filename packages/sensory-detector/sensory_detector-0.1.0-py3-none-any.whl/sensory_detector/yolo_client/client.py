import httpx
import asyncio
from typing import Optional, Union
from pathlib import Path
from src.sensory_detector.models.models import DetectionSeries, ModelsResponse

class YOLOAPIClient:
    """
    Гибкий клиент для асинхронного и синхронного взаимодействия с YOLO сервером.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    # ----- МОДЕЛИ -----
    async def get_available_models(self) -> ModelsResponse:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            r = await client.get("/api/available_models")
            r.raise_for_status()
            return ModelsResponse(**r.json())

    async def get_loaded_models(self) -> list[dict]:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            r = await client.get("/api/loaded_models")
            r.raise_for_status()
            return r.json()

    async def unload_model(self, model_name: str) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            r = await client.delete(f"/api/unload_model/{model_name}")
            r.raise_for_status()
            return r.json()

    # ----- АНАЛИЗ -----
    async def analyze_image(
        self,
        image: Union[str, Path],
        model_name: Optional[str] = None,
    ) -> DetectionSeries:
        """
        Отправить изображение (upload) для анализа.
        """
        image_path = Path(image)
        if not image_path.exists():
            raise FileNotFoundError(f"Файл не найден: {image_path}")

        files = {"file": (image_path.name, open(image_path, "rb"), "image/jpeg")}
        data = {}
        if model_name:
            data["model_name"] = model_name

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            r = await client.post("/api/analyze/auto", files=files, data=data)
            r.raise_for_status()
            return DetectionSeries(**r.json())

    async def analyze_video_upload(
        self,
        video: Union[str, Path],
        model_name: Optional[str] = None,
    ) -> DetectionSeries:
        """
        Отправить видео (upload) для анализа.
        """
        video_path = Path(video)
        if not video_path.exists():
            raise FileNotFoundError(f"Файл не найден: {video_path}")

        files = {"file": (video_path.name, open(video_path, "rb"), "video/mp4")}
        data = {}
        if model_name:
            data["model_name"] = model_name

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            r = await client.post("/api/analyze/auto", files=files, data=data)
            r.raise_for_status()
            return DetectionSeries(**r.json())

    async def analyze_by_path(
        self,
        file_path: Union[str, Path],
        model_name: Optional[str] = None,
    ) -> DetectionSeries:
        """
        Анализ по серверному пути (если FILES_PATH разрешён).
        """
        data = {"path": str(file_path)}
        if model_name:
            data["model_name"] = model_name
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            r = await client.post("/api/analyze/auto", data=data)
            r.raise_for_status()
            return DetectionSeries(**r.json())

    # ----- СИНХРОННЫЕ ОБЁРТКИ -----
    def sync(self):
        return YOLOAPIClientSync(self.base_url)

class YOLOAPIClientSync:
    """
    Синхронный клиент (на базе httpx).
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_available_models(self) -> ModelsResponse:
        with httpx.Client(base_url=self.base_url) as client:
            r = client.get("/api/available_models")
            r.raise_for_status()
            return ModelsResponse(**r.json())

    def get_loaded_models(self) -> list[dict]:
        with httpx.Client(base_url=self.base_url) as client:
            r = client.get("/api/loaded_models")
            r.raise_for_status()
            return r.json()

    def unload_model(self, model_name: str) -> dict:
        with httpx.Client(base_url=self.base_url) as client:
            r = client.delete(f"/api/unload_model/{model_name}")
            r.raise_for_status()
            return r.json()

    def analyze_image(self, image: Union[str, Path], model_name: Optional[str] = None) -> DetectionSeries:
        image_path = Path(image)
        if not image_path.exists():
            raise FileNotFoundError(f"Файл не найден: {image_path}")
        files = {"file": (image_path.name, open(image_path, "rb"), "image/jpeg")}
        data = {}
        if model_name:
            data["model_name"] = model_name
        with httpx.Client(base_url=self.base_url) as client:
            r = client.post("/api/analyze/auto", files=files, data=data)
            r.raise_for_status()
            return DetectionSeries(**r.json())

    def analyze_video_upload(self, video: Union[str, Path], model_name: Optional[str] = None) -> DetectionSeries:
        video_path = Path(video)
        if not video_path.exists():
            raise FileNotFoundError(f"Файл не найден: {video_path}")
        files = {"file": (video_path.name, open(video_path, "rb"), "video/mp4")}
        data = {}
        if model_name:
            data["model_name"] = model_name
        with httpx.Client(base_url=self.base_url) as client:
            r = client.post("/api/analyze/auto", files=files, data=data)
            r.raise_for_status()
            return DetectionSeries(**r.json())

    def analyze_by_path(self, file_path: Union[str, Path], model_name: Optional[str] = None) -> DetectionSeries:
        data = {"path": str(file_path)}
        if model_name:
            data["model_name"] = model_name
        with httpx.Client(base_url=self.base_url) as client:
            r = client.post("/api/analyze/auto", data=data)
            r.raise_for_status()
            return DetectionSeries(**r.json())