import asyncio
import atexit
import os
from typing import Optional

from .config import LokiLoggerOptions
from .flush_manager import AsyncFlushManager
from .interceptors import (intercept_exceptions, intercept_logging,
                           intercept_print)
from .safe_flush import safe_flush
from .utils import now_ns, safe_json


class LokiLogger:
    def __init__(self, options: LokiLoggerOptions):
        self.options = options
        self.log_buffer: list[tuple[str, str]] = []
        self.flush_manager = AsyncFlushManager(self)
        intercept_print(self)
        intercept_logging(self)
        intercept_exceptions(self)
        if os.getenv("RUN_MAIN") == "true" or not os.getenv("RUN_MAIN"):
            atexit.register(lambda: safe_flush(self))

    def track_event(self, event_name: str, properties: Optional[dict] = None) -> None:
        ts = now_ns()
        message = f"[EVENT] {event_name} {safe_json(properties)}" if properties else f"[EVENT] {event_name}"
        self.log_buffer.append((ts, message))
        self.flush_manager.check_and_flush()

    async def flush_logs(self) -> None:
        if not self.log_buffer:
            return
        buffer_copy = self.log_buffer.copy()
        self.log_buffer.clear()
        await self.flush_manager.send_logs(buffer_copy)

    def flush_sync(self):
        try:
            asyncio.run(self.flush_logs())
        except RuntimeError:
            pass
