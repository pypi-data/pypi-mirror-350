import json
import time


def now_ns() -> str:
    return str(int(time.time() * 1_000_000_000))

def safe_json(data) -> str:
    try:
        return json.dumps(data)
    except Exception:
        return "{}"

def get_labels(options):
    try:
        dynamic_labels = {
            k: str(v()) for k, v in options.dynamic_labels.items()
        }
    except Exception:
        dynamic_labels = {}
    return {
        "app": options.app_name,
        **options.labels,
        **dynamic_labels,
    }
