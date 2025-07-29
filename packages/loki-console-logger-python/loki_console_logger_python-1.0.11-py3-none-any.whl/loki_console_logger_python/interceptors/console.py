import builtins
from time import time_ns

def intercept_print(logger):
    original_print = builtins.print

    def custom_print(*args, **kwargs):
        ts = str(time_ns())
        message = " ".join(str(a) for a in args)
        logger.log_buffer.append((ts, f"[PRINT] {message}"))
        logger.flush_manager.check_and_flush()
        original_print(*args, **kwargs)

    builtins.print = custom_print
