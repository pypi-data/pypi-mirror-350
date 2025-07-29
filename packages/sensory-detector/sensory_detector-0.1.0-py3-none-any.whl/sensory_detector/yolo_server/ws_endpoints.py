# yolo_server/ws_endpoints.py
from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Query
import cv2, numpy as np, logging, json
import asyncio # Нужен для asyncio.to_thread
from typing import List # Явный импорт List

# Импорты моделей
from src.sensory_detector.models.models import DetectedObject, BoundingBox, DetectionFrame # Добавим DetectionFrame если нужно

# Импорт кэша
from src.sensory_detector.yolo_server.cache_manager import model_cache # Теперь model_cache импортируется из cache_manager

log = logging.getLogger(__name__)

ws_router = APIRouter()

def _serialize(dets: list[DetectedObject]) -> list[dict]:
    """Сериализует список DetectedObject в список словарей для JSON."""
    # Используем model_dump для Pydantic v2
    # Если используется Pydantic v1, нужно использовать .dict()
    # Проверяем наличие метода, чтобы быть совместимым
    if hasattr(DetectedObject, 'model_dump'):
        return [d.model_dump() for d in dets] # type: ignore
    else:
        return [d.dict() for d in dets] # type: ignore # Для Pydantic v1


@ws_router.websocket("/ws/analyze")
async def analyze_stream(
    websocket: WebSocket,
    model_name: str | None = Query(None, description="Опционально выбрать модель для анализа"),
):
    """
    WebSocket эндпоинт для потокового анализа кадров.
    Клиент присылает бинарные данные изображения (JPEG/PNG) для каждого кадра.
    Сервер отвечает JSON-объектом с результатами детекции для этого кадра.

    Формат сообщения клиента:
        b'<binary image bytes>'

    Формат ответа сервера (JSON):
        {
          "index": <int>,        # счетчик кадров, начиная с 0
          "timestamp": <float>,  # примерная отметка времени (index / fps)
          "detections": [...]    # список обнаруженных объектов (DetectedObject)
        }
    """
    await websocket.accept()
    detector = None # Инициализируем детектор перед try блоком
    frame_idx = 0

    log.info(f"WebSocket connection accepted. Model requested: {model_name}")

    try:
        # Получаем детектор. Это может вызвать исключения, ловим их.
        detector = await model_cache.get(model_name)
        log.info(f"WebSocket using model: {detector.model_name()}")

        while True:
            # Ждем следующий кадр от клиента
            data = await websocket.receive_bytes()
            log.debug(f"Received {len(data)} bytes for frame {frame_idx}")

            if not data:
                 # Клиент может отправить пустые данные перед отключением
                 log.debug("Received empty bytes, client likely disconnecting.")
                 break # Выходим из цикла

            # ─ 1. Декодируем bytes → numpy array (блокирующая операция)
            # Выполняем в отдельном потоке, чтобы не блокировать event loop
            nparr = np.frombuffer(data, np.uint8)
            frame = await asyncio.to_thread(cv2.imdecode, nparr, cv2.IMREAD_COLOR)

            if frame is None:
                log.warning(f"Failed to decode image data for frame {frame_idx}. Sending error.")
                await websocket.send_json({"index": frame_idx, "error": "Bad image data"})
                # Возможно, стоит пропустить этот кадр и ждать следующий, или закрыть соединение?
                # Пропускаем и ждем следующий.
                frame_idx += 1 # Увеличиваем счетчик даже при ошибке, чтобы индекс в ответе был корректным
                continue

            # ─ 2. Запускаем детектор (CPU/GPU-bound операция)
            # Также выполняем в отдельном потоке
            # Примерная отметка времени: frame_idx / 30.0 (если считать 30 fps)
            # Лучше бы получать timestamp от клиента, если он есть
            timestamp = float(frame_idx / 30.0) # Предполагаем 30 FPS для timestamp
            log.debug(f"Running detection for frame {frame_idx} at approx {timestamp:.2f}s")
            detections = await asyncio.to_thread(
                detector.detect_from_frame, frame, timestamp
            )
            log.debug(f"Detection complete for frame {frame_idx}. Found {len(detections)} objects.")


            # ─ 3. Отправляем результат клиенту
            response_data = {
              "index": frame_idx,
              "timestamp": timestamp,
              "detections": _serialize(detections)
            }
            await websocket.send_json(response_data)

            frame_idx += 1

    except WebSocketDisconnect as e:
        # Клиент корректно отключился
        log.info(f"WebSocket client disconnected. Code: {e.code}, Reason: {e.reason}")
        # Не нужно вызывать websocket.close() здесь, Starlette сделает это автоматически
    except (ValueError, FileNotFoundError, RuntimeError) as e:
         # Ошибки при получении/загрузке модели
         log.error(f"Error getting model for WS: {e}", exc_info=True)
         await websocket.send_json({"error": f"Server error: {e}"})
         await websocket.close(code=1011) # Internal Error
    except Exception as e:
        # Любые другие необработанные исключения
        log.exception("Unexpected error in WebSocket stream: %s", e)
        await websocket.send_json({"error": "Internal server error"})
        await websocket.close(code=1011) # Internal Error

    finally:
        # Логика cleanup, если потребуется (например, выгрузка модели, если она была загружена только для этого соединения)
        # В текущей архитектуре кэша, модель выгрузится по таймауту, так что явный cleanup не нужен.
        log.info(f"WebSocket handler finished for model {detector.model_name() if detector else 'N/A'}. Total frames: {frame_idx}")