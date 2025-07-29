import logging
from time import time_ns

class LokiHandler(logging.Handler):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def emit(self, record):
        try:
            ts = str(time_ns())
            msg = self.format(record)
            self.logger.log_buffer.append((ts, f"[{record.levelname}] {msg}"))
            self.logger.flush_manager.check_and_flush()
        except Exception:
            pass

def intercept_logging(logger):
    handler = LokiHandler(logger)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.basicConfig(level=logging.INFO, handlers=[handler])
