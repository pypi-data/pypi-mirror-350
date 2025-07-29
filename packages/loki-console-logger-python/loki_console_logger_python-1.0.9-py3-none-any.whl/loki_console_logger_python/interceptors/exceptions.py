import sys
import traceback
import asyncio
from time import time_ns

def intercept_exceptions(logger):
    original_hook = sys.excepthook

    def custom_hook(exc_type, exc_value, exc_traceback):
        ts = str(time_ns())
        error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.log_buffer.append((ts, f"[EXCEPTION] {error_message}"))
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(logger.flush_logs())
            else:
                asyncio.run(logger.flush_logs())
        except Exception:
            pass  

        original_hook(exc_type, exc_value, exc_traceback)

    sys.excepthook = custom_hook
