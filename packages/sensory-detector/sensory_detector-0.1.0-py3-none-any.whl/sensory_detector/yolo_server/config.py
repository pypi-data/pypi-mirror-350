import os
from pathlib import Path
from dotenv import load_dotenv
# project_root/yolo_server/config.py
import os
from pathlib import Path
# from dotenv import load_dotenv # Pydantic BaseSettings can handle this
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PositiveInt, DirectoryPath # Add DirectoryPath validation
from typing import Optional, Any

class Config(BaseSettings):
    
    PROJECT_ROOT: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent,
        description="Корень проекта",
    )
    WEIGHTS_DIR: Path = Field(
        default="weights",
        description="Каталог с .pt-весами моделей",
    )
    FILES_PATH: Optional[DirectoryPath] = Field(
        default=None,
        description="Каталог, из которого разрешается анализ по видео",
    )
    
    MODEL_CACHE_TIMEOUT_SEC: PositiveInt = Field(
            default=30,
            description="Через сколько секунд простоя выгружать модель из памяти GPU",
    )
    DEFAULT_MODEL_NAME: str = Field(default="yolov8s")
    DEFAULT_MODEL_PATH: Path | None = None 

    def __init__(self, **data):
        # Сначала даём BaseSettings заполнить поля из env / дефолтов
        load_dotenv()  # если нужен dotenv – можно оставить
        super().__init__(**data)
        
        self.WEIGHTS_DIR = (self.PROJECT_ROOT / self.WEIGHTS_DIR).resolve()
        self.DEFAULT_MODEL_PATH = self.WEIGHTS_DIR / f"{self.DEFAULT_MODEL_NAME}.pt"

        # Создаём каталог с весами, если его нет
        self.WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

        # FILES_PATH может быть None или относительным
        if self.FILES_PATH is not None:
            self.FILES_PATH = Path(self.FILES_PATH).resolve()


config = Config()
