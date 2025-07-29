
import asyncio, logging, psutil, gc
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Callable, TypeVar, Generic, List, Any
from contextlib import suppress
import os
from src.sensory_detector.yolo_server.config import config
from src.sensory_detector.yolo_server.detectors.detector_interface import Detector
from src.sensory_detector.yolo_server.detectors.yolo_wrapper import YOLOv8Wrapper
from src.sensory_detector.yolo_server.detectors.clip_wrapper import CLIPWrapper
try:
    import torch
    _torch_available = True
except ImportError:
    _torch_available = False
    
log = logging.getLogger(__name__)
T = TypeVar("T", bound=Detector)

MODEL_WRAPPERS = {
    "yolov8s": YOLOv8Wrapper,
    "clip-base": CLIPWrapper,
    # ...
}
# ──────────────────────────────────────────────────────────────────────────
# DATA CLASSES
# ──────────────────────────────────────────────────────────────────────────
@dataclass
class _CacheItem(Generic[T]):
    wrapper: T
    last_used: datetime
    hits: int = 0


# ──────────────────────────────────────────────────────────────────────────
# MAIN CACHE
# ──────────────────────────────────────────────────────────────────────────
class ModelCache(Generic[T]):
    """LRU-кэш для детекторов"""

    def __init__(self, ttl_sec: int = 30, max_models: int = 10):
        self.ttl = timedelta(seconds=ttl_sec)
        self.max_models = max_models
        self._cache: Dict[str, _CacheItem[T]] = {}
        self._lock = asyncio.Lock()
        self._reaper_task: asyncio.Task | None = None

    # public ────────────────────────────────────────────────────────────
    async def start(self):
        if not self._reaper_task:
            self._reaper_task = asyncio.create_task(self._reaper())

    async def shutdown(self):
        if self._reaper_task:
            self._reaper_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._reaper_task
        async with self._lock:
            for item in self._cache.values():
                item.wrapper.unload()
            self._cache.clear()
            gc.collect()
            if _torch_available and torch.cuda.is_available():
                try:
                    torch.cuda.empty_cache()
                    log.debug("torch.cuda.empty_cache() called during shutdown.")
                except Exception as e:
                    log.warning(f"Error calling torch.cuda.empty_cache() during shutdown: {e}")


    async def get(
        self,
        name: str | None = None,
        loader: Callable[[str], T] | None = None,
    ) -> T:
        """
        Возвращает детектор из кэша или загружает его.
        Обновляет метки использования.
        """
        name = name or config.DEFAULT_MODEL_NAME
        if not name:
             raise ValueError("Model name must be provided or DEFAULT_MODEL_NAME must be set in config.")

        loader = MODEL_WRAPPERS.get(name, YOLOv8Wrapper) # Используем YOLOv8Wrapper как загрузчик по умолчанию

        async with self._lock:
            # ─ hit ────────────────────────────────────────────────────────
            if name in self._cache:
                item = self._cache[name]
                item.last_used = datetime.now()
                item.hits += 1
                log.debug(f"Cache HIT for model '{name}'. Hits: {item.hits}")
                return item.wrapper

            # ─ miss ───────────────────────────────────────────────────────
            log.info(f"Cache MISS for model '{name}'. Loading...")
            if len(self._cache) >= self.max_models:
                log.warning(f"Cache is full ({len(self._cache)} models). Evicting oldest...")
                await self._evict_one_locked()

            try:
                # Загрузка модели может быть долгой и/или CPU-bound, выполняем в отдельном потоке
                wrapper = await asyncio.to_thread(loader, name)
                self._cache[name] = _CacheItem(
                    wrapper=wrapper, last_used=datetime.now(), hits=1
                )
                log.info(f"Model '{name}' loaded and added to cache. Current cache size: {len(self._cache)}")
                return wrapper
            except FileNotFoundError as e:
                 log.error(f"Model file not found for '{name}': {e}")
                 raise FileNotFoundError(f"Model '{name}' not found. Ensure '{name}.pt' is in {config.WEIGHTS_DIR}") from e
            except Exception as e:
                log.error(f"Failed to load model '{name}': {e}", exc_info=True)
                raise RuntimeError(f"Failed to load model '{name}'. See logs for details.") from e



    async def stats(self) -> List[dict[str, Any]]:
        async with self._lock:
            now = datetime.now()
            data = []
            for name, item in self._cache.items():
                data.append(
                    {
                        "model_name": name,
                        "wrapper_class": item.wrapper.__class__.__name__,
                        "last_used": item.last_used.isoformat(),
                        "idle_seconds": round((now - item.last_used).total_seconds(), 1),
                        "hits": item.hits,
                        "mem_bytes": self._mem_estimate(item.wrapper),
                    }
                )
            return data

    # internal ─────────────────────────────────────────────────────────
    async def _reaper(self):
        """Фоновая задача для выгрузки старых моделей."""
        while True:
            await asyncio.sleep(self.ttl.total_seconds())
            log.debug("Cache reaper running...")
            cutoff = datetime.now() - self.ttl
            async with self._lock:
                names_to_evict = [
                    name for name, item in self._cache.items()
                    if item.last_used < cutoff
                ]
                if names_to_evict:
                    log.info(f"Reaper evicting {len(names_to_evict)} models due to timeout.")
                for name in names_to_evict:
                    item = self._cache.pop(name)
                    try:
                        item.wrapper.unload()
                        log.info("Model '%s' evicted after idle timeout (%s secs).", name, self.ttl.total_seconds())
                    except Exception as e:
                        log.error(f"Error unloading model '{name}' during reaper: {e}", exc_info=True)



    async def _evict_one_locked(self):
        """Выгружает одну модель (наименее недавно использовавшуюся). Требует, чтобы lock был уже взят."""
        if not self._cache:
            log.warning("Eviction requested, but cache is empty.")
            return # Ничего делать, если кэш пуст

        # LRU: ищем самый старый last_used
        oldest_name = min(self._cache, key=lambda k: self._cache[k].last_used)
        item = self._cache.pop(oldest_name)
        try:
            item.wrapper.unload()
            log.info("Model '%s' evicted because cache is full (%s/%s models).",
                     oldest_name, len(self._cache)+1, self.max_models)
        except Exception as e:
             log.error(f"Error unloading model '{oldest_name}' during eviction: {e}", exc_info=True)


    # static helpers ──────────────────────────────────────────────────
    @staticmethod
    def _mem_estimate(wrapper: Detector) -> int:
        """
        Универсальная оценка VRAM/RAM, занимаемой оберткой детектора.
        1. wrapper.mem_bytes()          – если детектор сам умеет считать (приоритет)
        2. torch.cuda.memory_allocated  – когда под капотом PyTorch/CUDA
        3. psutil RSS                   – как последний резерв (RSS всего процесса)
        Возвращает байты.
        """
        # 1. user-defined hook (если обертка предоставляет свой метод)
        if hasattr(wrapper, "mem_bytes") and callable(wrapper.mem_bytes):
            try:
                mem = wrapper.mem_bytes()
                if isinstance(mem, (int, float)):
                     return int(mem)
                log.warning(f"wrapper.mem_bytes() returned non-numeric value: {mem}")
            except Exception as e:
                log.warning(f"Error calling wrapper.mem_bytes(): {e}", exc_info=True)

        # 2. PyTorch / CUDA (если обертка содержит torch модель на CUDA)
        if _torch_available:
            try:
                mdl = getattr(wrapper, "model", None)
                if mdl is not None and hasattr(mdl, "to") and hasattr(mdl, "device") and mdl.device.type == "cuda":
                    # Check if it's a PyTorch model on CUDA
                    return int(torch.cuda.memory_allocated(mdl.device))
            except Exception as e:
                log.warning(f"Error estimating torch CUDA memory: {e}", exc_info=True)

        # 3. RSS процесса (fallback)
        try:
            return psutil.Process(os.getpid()).memory_info().rss
        except Exception as e:
             log.warning(f"Error estimating process RSS: {e}", exc_info=True)
             return 0 # Не удалось оценить память

    async def _async_update_activity(self, name: str):
        """Обновляет метку last_used для модели в кэше."""
        # Этот метод предназначен для вызова из async контекста или через run_coroutine_threadsafe
        async with self._lock:
            if name in self._cache:
                self._cache[name].last_used = datetime.now()
                # log.debug(f"Activity updated for model '{name}'.") # Может быть слишком много логов
            else:
                # Это может случиться, если модель была выгружена другим способом
                log.debug(f"Activity update requested for model '{name}', but it's not in cache.")


# глобальный синглтон кэша
model_cache: ModelCache[Detector] = ModelCache(
    ttl_sec=int(config.MODEL_CACHE_TIMEOUT_SEC)
    if hasattr(config, "MODEL_CACHE_TIMEOUT_SEC")
    else 30,
    max_models=int(10)
    if hasattr(config, "MODEL_CACHE_MAX")
    else 10,
)