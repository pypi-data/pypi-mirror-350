import asyncio
import threading


def safe_flush(logger):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(logger.flush_logs())
        else:
            asyncio.run(logger.flush_logs())
    except RuntimeError:
        threading.Thread(target=lambda: asyncio.run(logger.flush_logs())).start()
