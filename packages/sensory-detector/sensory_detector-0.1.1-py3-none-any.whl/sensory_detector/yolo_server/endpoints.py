# yolo_server/endpoints.py
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Query, Path as FastAPIPath
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder # Для ручной сериализации, если pydantic не справляется
from typing import Optional, List, Annotated
import mimetypes, tempfile, os, logging
from pathlib import Path
import av # Необходим для определения типа видео
import asyncio # Необходим для await в analyze_auto
import shutil # Для асинхронного копирования файла
import cv2
# Импорты моделей
from src.sensory_detector.models.models import (
    ModelsResponse,
    DetectedObject,
    BoundingBox,
    DetectionFrame,
    DetectionSeries,
    CacheStatsResponse,
    UnloadModelResponse # Добавим эту модель
)

# Импорты из нашего проекта
from src.sensory_detector.yolo_server.cache_manager import model_cache
from src.sensory_detector.yolo_server.config import config
# Убедимся, что импортируем process_video_sync из правильного места
from src.sensory_detector.yolo_server.video_analizer.video_processor import process_video_sync # <<< Correct import

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["yolo"])

def _scan_weights() -> List[str]:
    """Сканирует каталог весов и возвращает список имен моделей без расширения."""
    weights_dir = config.WEIGHTS_DIR
    if not weights_dir.exists():
        logger.warning(f"Weights directory not found: {weights_dir}")
        return []
    try:
        # Используем list comprehension для эффективности
        model_names = [
            f.stem for f in weights_dir.iterdir()
            if f.is_file() and f.suffix == ".pt"
        ]
        logger.debug(f"Found {len(model_names)} model files in {weights_dir}")
        return model_names
    except Exception as e:
        logger.error(f"Error scanning weights directory {weights_dir}: {e}", exc_info=True)
        return []


# --------------- API Endpoints -----------------

@router.get(
    "/available_models",
    response_model=ModelsResponse,
    summary="Получить список доступных моделей"
)
async def available_models():
    """
    Возвращает список имен моделей, файлы которых (.pt) найдены
    в сконфигурированном каталоге весов (WEIGHTS_DIR).
    """
    logger.info("Request received for available_models")
    return ModelsResponse(
        available_models=_scan_weights(),
        default_model=config.DEFAULT_MODEL_NAME,
        message="Выберите модель по имени. Если имя не указано в запросе, будет использована модель по умолчанию."
    )

@router.get(
    "/loaded_models",
    response_model=List[CacheStatsResponse],
    summary="Получить статус загруженных моделей в кэше"
)
async def loaded_models():
    """
    Возвращает текущий статус кэша моделей: какие модели загружены,
    сколько секунд простаивают, сколько раз использовались,
    и примерную занимаемую память (VRAM/RAM).
    """
    logger.info("Request received for loaded_models (cache status)")
    return await model_cache.stats()

@router.delete(
    "/unload_model/{model_name}",
    response_model=UnloadModelResponse,
    summary="Принудительно выгрузить модель из кэша"
)
async def unload_model(
    model_name: Annotated[
        str, FastAPIPath(..., description="Имя модели (без расширения .pt)")
    ]
):
    """
    Принудительно выгружает указанную модель из кэша.
    Полезно для освобождения памяти или при обновлении файла весов.
    """
    logger.info(f"Request received to unload model: {model_name}")
    # Логика выгрузки уже есть в cache_manager._evict_one_locked, но там она приватная.
    # Лучше добавить публичный метод или адаптировать.
    # Пока используем прямой доступ для быстрого исправления, но это следует рефакторить
    # в публичный метод model_cache.unload_model(name)
    async with model_cache._lock:  # !!! Pylint warning, needs refactor in ModelCache
        item = model_cache._cache.pop(model_name, None)
        if not item:
            logger.warning(f"Unload requested for model '{model_name}', but it was not found in cache.")
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found in cache.")
        try:
            item.wrapper.unload()
            logger.info(f"Successfully unloaded model: {model_name}")
            return {"detail": f"Model '{model_name}' was unloaded from cache."}
        except Exception as e:
            logger.error(f"Error during manual unload of model '{model_name}': {e}", exc_info=True)
            # Хотя модель уже удалена из кэша, сообщим об ошибке выгрузки
            raise HTTPException(status_code=500, detail=f"Error unloading model '{model_name}'. See server logs.")


@router.post(
    "/analyze/auto",
    response_model=DetectionSeries, # Используем DetectionSeries для единообразия
    summary="Анализ изображения или видео (upload или по пути)"
)
async def analyze_auto(
    file: UploadFile | None = File(None, description="Картинка или видео файл для загрузки"),
    path: str | None = Form(
        None, description=f"Абсолютный или относительный путь до файла в разрешенной директории ({config.FILES_PATH}). Доступно, только если FILES_PATH сконфигурирован."
    ),
    model_name: str | None = Form(None, description="Имя модели (без .pt). Если не указано, используется модель по умолчанию.")
):
    """
    Универсальный эндпоинт для анализа. Принимает файл по HTTP Upload
    или путь к файлу на сервере (если разрешено конфигом FILES_PATH).
    Автоматически определяет тип файла (изображение или видео) и выполняет анализ.
    """
    if not file and not path:
        raise HTTPException(
            status_code=422, detail="Необходимо предоставить либо 'file' (HTTP upload), либо 'path' (путь к файлу на сервере)."
        )

    if file and path:
        # Избегаем неоднозначности
         raise HTTPException(
             status_code=422, detail="Пожалуйста, предоставьте либо 'file', либо 'path', но не оба одновременно."
         )

    logger.info(f"Analysis request: file={file.filename if file else None}, path={path}, model={model_name}")

    # 0. Получаем детектор из кэша
    try:
        detector = await model_cache.get(model_name)
        logger.debug(f"Using model: {detector.model_name()}")
    except (ValueError, FileNotFoundError, RuntimeError) as e:
         logger.error(f"Failed to get model '{model_name}': {e}", exc_info=True)
         raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
         logger.error(f"An unexpected error occurred getting model '{model_name}': {e}", exc_info=True)
         raise HTTPException(status_code=500, detail="Internal server error while loading model.")


    # 1. Анализ UploadFile ───────────────────────────────────────────
    if file:
        content_type = file.content_type
        filename = file.filename or "upload"
        logger.info(f"Processing uploaded file: {filename}, content_type: {content_type}")

        if not content_type:
             # Попробуем угадать по расширению как fallback
             content_type, _ = mimetypes.guess_type(filename)
             if not content_type:
                logger.warning(f"Could not determine content type for {filename}")
                raise HTTPException(status_code=400, detail="Cannot determine file type from Content-Type or filename.")

        if content_type.startswith("image/"):
            logger.debug("Detected image upload.")
            try:
                img_bytes = await file.read() # Асинхронное чтение всего файла в память
                detections = await asyncio.to_thread(detector.detect_from_bytes, img_bytes) # CPU-bound детекция в треде
                # Для одиночного изображения, заворачиваем в формат DetectionSeries
                return DetectionSeries(
                    model_name=detector.model_name(),
                    detections=[DetectionFrame(index=0, timestamp=0.0, detections=detections)],
                )
            except Exception as e:
                 logger.error(f"Error processing image upload: {e}", exc_info=True)
                 raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

        if content_type.startswith("video/"):
            logger.debug("Detected video upload. Saving to temp file for processing.")
            # Сохраняем видео во временный файл асинхронно
            # Использование tempfile.NamedTemporaryFile с delete=False безопасно, т.к. мы его явно удаляем
            suffix = Path(filename).suffix if filename else ".mp4" # Добавляем суффикс, если имя есть
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp_path = Path(tmp.name)
                while True:
                    chunk = await file.read(1024 * 1024)
                    if not chunk:
                        break
                    tmp.write(chunk)
                tmp.flush()
                logger.info(f"Uploaded video saved to temporary file: {tmp_path}")

            try:
                # Обработка видео - это блокирующая операция, выполняем в thread pool
                frames = await asyncio.to_thread(process_video_sync, str(tmp_path), detector)
                logger.info(f"Finished processing temporary video file: {tmp_path}")
                return DetectionSeries(
                    model_name=detector.model_name(),
                    detections=frames,
                )
            except (ValueError, IOError, RuntimeError) as e:
                 logger.error(f"Error processing temporary video file {tmp_path}: {e}", exc_info=True)
                 raise HTTPException(status_code=500, detail=f"Error processing video: {e}")
            except Exception as e:
                 logger.error(f"An unexpected error occurred processing temporary video file {tmp_path}: {e}", exc_info=True)
                 raise HTTPException(status_code=500, detail="Internal server error during video processing.")
            finally:
                # Обязательно удаляем временный файл
                if tmp_path.exists():
                    try:
                        os.unlink(tmp_path)
                        logger.debug(f"Temporary file deleted: {tmp_path}")
                    except Exception as e:
                        logger.warning(f"Failed to delete temporary file {tmp_path}: {e}")


        # Если тип не изображение и не видео
        logger.warning(f"Unsupported MIME type uploaded: {content_type}")
        raise HTTPException(status_code=400, detail=f"Unsupported MIME type: {content_type}")


    # 2. Анализ по path ──────────────────────────────────────────────
    if path:
        logger.info(f"Processing file from path: {path}")

        if config.FILES_PATH is None:
             logger.warning(f"Path-based access requested for '{path}', but FILES_PATH is not configured.")
             raise HTTPException(
                 status_code=403,
                 detail="Доступ к файлам по пути на сервере отключен в конфигурации (FILES_PATH не задан)."
             )

        # Безопасная нормализация и проверка пути
        # 1. Нормализуем путь относительно FILES_PATH
        # 2. Проверяем, что результирующий абсолютный путь НАЧИНАЕТСЯ с FILES_PATH
        try:
            # Используем Pathlib для нормализации и резолвинга
            requested_path = Path(path)
            if not requested_path.is_absolute():
                 # Если путь относительный, считаем его относительно FILES_PATH
                 absolute_path = (config.FILES_PATH / requested_path).resolve()
            else:
                 # Если путь абсолютный, просто резолвим (разрешает симлинки и прочее)
                 absolute_path = requested_path.resolve()

            # Самая важная проверка безопасности
            if not str(absolute_path).startswith(str(config.FILES_PATH)):
                logger.warning(f"Path traversal attempt detected! Resolved path '{absolute_path}' is outside allowed dir '{config.FILES_PATH}' for requested path '{path}'.")
                raise HTTPException(
                    status_code=403,
                    detail=f"Доступ к пути '{path}' запрещен. Путь должен находиться внутри разрешенной директории '{config.FILES_PATH}'."
                )

            if not absolute_path.exists():
                logger.warning(f"Requested file not found at resolved path: {absolute_path}")
                raise HTTPException(status_code=404, detail=f"Файл '{path}' не найден.")

            if not absolute_path.is_file():
                logger.warning(f"Requested path is not a file: {absolute_path}")
                raise HTTPException(status_code=400, detail=f"Путь '{path}' не является файлом.")

            final_path = str(absolute_path)
            logger.debug(f"Resolved and validated path: {final_path}")

        except Exception as e:
             logger.error(f"Path validation failed for '{path}': {e}", exc_info=True)
             # Отлавливаем ошибки Pathlib и любые другие ошибки обработки пути
             raise HTTPException(status_code=400, detail=f"Ошибка при обработке пути: {e}")


        # Определяем тип файла по расширению или pyAV
        mime_type, _ = mimetypes.guess_type(final_path)
        is_image = mime_type and mime_type.startswith("image/")
        is_video = mime_type and mime_type.startswith("video/")

        # Fallback для видео, если mimetypes не сработал
        if not is_image and not is_video:
             logger.debug(f"mimetypes could not determine type for {final_path}, trying pyAV...")
             try:
                 # Попытка открыть pyAV контейнер - это блокирующая операция,
                 # но она быстрая для определения формата. Выполним в треде.
                 # Если успешно - это видео.
                 container = await asyncio.to_thread(av.open, final_path)
                 container.close() # Закрываем сразу, нам нужен только факт открытия
                 is_video = True
                 logger.debug(f"pyAV confirmed {final_path} is a video.")
             except av.AVError:
                 # Если pyAV не смог открыть, возможно это не видео (или не поддерживаемый формат)
                 logger.debug(f"pyAV failed to open {final_path}, assuming not a video.")
                 pass # Не видео

        if is_image:
             logger.debug(f"Detected image file via path: {final_path}")
             try:
                # Чтение изображения также блокирующее, но обычно быстрое
                img = await asyncio.to_thread(cv2.imread, final_path)
                if img is None:
                    logger.error(f"cv2.imread failed for image file: {final_path}")
                    raise HTTPException(status_code=500, detail=f"Не удалось прочитать изображение по пути: {path}")

                detections = await asyncio.to_thread(detector.detect_from_frame, img, 0.0) # 0.0 timestamp для изображения
                # Заворачиваем результат для изображения в DetectionSeries
                return DetectionSeries(
                    model_name=detector.model_name(),
                    detections=[DetectionFrame(index=0, timestamp=0.0, detections=detections)],
                )
             except Exception as e:
                 logger.error(f"Error processing image file from path {final_path}: {e}", exc_info=True)
                 raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения по пути '{path}': {e}")


        elif is_video:
             logger.debug(f"Detected video file via path: {final_path}")
             try:
                # Обработка видео - блокирующая и долгая операция, выполняем в thread pool
                frames = await asyncio.to_thread(process_video_sync, final_path, detector)
                logger.info(f"Finished processing video file from path: {final_path}")
                return DetectionSeries(
                    model_name=detector.model_name(),
                    detections=frames,
                )
             except (ValueError, IOError, RuntimeError) as e:
                 logger.error(f"Error processing video file from path {final_path}: {e}", exc_info=True)
                 raise HTTPException(status_code=500, detail=f"Ошибка при обработке видео по пути '{path}': {e}")
             except Exception as e:
                 logger.error(f"An unexpected error occurred processing video file from path {final_path}: {e}", exc_info=True)
                 raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера при обработке видео по пути.")

        else:
             logger.warning(f"Unsupported file type detected for path: {final_path} (MIME: {mime_type})")
             raise HTTPException(status_code=400, detail=f"Неподдерживаемый тип файла по пути '{path}'. Ожидается изображение или видео.")