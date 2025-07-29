import asyncio
import time
from typing import Optional

FLUSH_INTERVAL_SECONDS = 2


class AsyncFlushManager:
    def __init__(self, logger):
        self.logger = logger
        self._last_flush = 0
        self._flush_task: Optional[asyncio.Task] = None

    def check_and_flush(self):
        now = time.time()
        if now - self._last_flush >= FLUSH_INTERVAL_SECONDS:
            self._last_flush = now
            self._schedule_flush()

    def _schedule_flush(self):
        try:
            loop = asyncio.get_running_loop()
            self._flush_task = loop.create_task(self._delayed_flush())
        except RuntimeError:
            self.logger.flush_sync()

    async def _delayed_flush(self):
        await asyncio.sleep(0.1)
        await self.logger.flush_logs()