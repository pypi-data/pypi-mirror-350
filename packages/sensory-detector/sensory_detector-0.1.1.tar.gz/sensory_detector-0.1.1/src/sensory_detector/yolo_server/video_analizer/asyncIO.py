"""
Адаптер: превращает асинхронный UploadFile в «синхронный» file-like
объект, который умеет читать данные по мере поступления.
Используется для скармливания pyAV без создания временных файлов.
"""
from __future__ import annotations

import io, asyncio, logging

log = logging.getLogger(__name__)


class AsyncIOWrapper(io.RawIOBase):
    CHUNK = 65_536  # 64 KB

    def __init__(self, uploader, loop: asyncio.AbstractEventLoop, chunk: int = CHUNK):
        from starlette.datastructures import UploadFile  # локальный импорт

        if not isinstance(uploader, UploadFile):
            raise TypeError("uploader must be UploadFile")

        self.uploader = uploader
        self.loop = loop
        self.chunk = chunk
        self._queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._eof = False

        # background producer
        self._producer_task = loop.create_task(self._producer())

    # producer: читает body и кладёт в очередь
    async def _producer(self):
        try:
            async for chunk in self.uploader.stream(self.chunk):
                await self._queue.put(chunk)
        finally:
            self._eof = True
            await self._queue.put(b"")  # EOF-маркер

    # sync read – pyAV будет звать из thread-pool
    def read(self, n: int = -1) -> bytes | None:  # type: ignore[override]
        fut = asyncio.run_coroutine_threadsafe(self._queue.get(), self.loop)
        data = fut.result()
        return data

    def close(self):
        if not self._producer_task.done():
            self._producer_task.cancel()