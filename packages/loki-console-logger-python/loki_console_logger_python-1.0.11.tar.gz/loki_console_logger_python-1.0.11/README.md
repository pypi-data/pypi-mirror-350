# Loki Console Logger for Python 🚀

![](https://badge.fury.io/py/loki-console-logger-python.svg)

![](https://img.shields.io/pypi/pyversions/loki-console-logger-python.svg)

[](https://img.shields.io/github/license/elvenobservability/loki-console-logger-python)

A **high-performance** console logger for Python that automatically sends all `print`, `logging`, unhandled exceptions, and custom events to **Grafana Loki** — powered by `asyncio` + `aiohttp`.

✅ Ideal for microservices, observability pipelines, cloud apps, and scripts.

🌀 Compatible with both **async** (FastAPI, asyncio) and **sync** (scripts, Django, etc.) environments.

---

## ✨ Features

- ⚡ Ultra-performant (fully async using `aiohttp`)
- 🧠 Dynamic + static labels support (e.g., env, hostname, region)
- 🧹 Batching + auto-flush for performance and throughput
- 🔗 Automatically captures:
    - `print(...)` calls
    - `logging` messages
    - uncaught exceptions
- 🔒 Optional `Authorization` header + multi-tenancy (`X-Scope-OrgID`)
- 🧱 Zero external dependencies (only `aiohttp`)
- 🧘 Safe fallback for **synchronous** apps (auto flush on shutdown)

---

## 📦 Installation

```bash
pip install loki-console-logger-python
```

---

## 🚀 Quickstart (Async Example)

```python
from loki_console_logger_python import LokiLogger
from loki_console_logger_python.config import LokiLoggerOptions

options = LokiLoggerOptions(
    url="https://loki.elvenobservability.com/loki/api/v1/push",
    tenant_id="your-tenant-id",
    app_name="my-app",
    auth_token="your-optional-token",
    labels={"env": "production"},
    dynamic_labels={"hostname": lambda: "my-host"},
)

logger = LokiLogger(options)

# Track custom events
logger.track_event("user_signup", {"user_id": 123})

# This will be captured automatically
print("✅ Hello from Python!")

# This will also be captured
import logging
logging.info("App started")

# So will uncaught exceptions
raise RuntimeError("Simulated failure")
```

---

## 🧱 Example with FastAPI

```python
from fastapi import FastAPI
from loki_console_logger_python import LokiLogger
from loki_console_logger_python.config import LokiLoggerOptions

app = FastAPI()

logger = LokiLogger(LokiLoggerOptions(
    url="https://loki.elvenobservability.com/loki/api/v1/push",
    tenant_id="elven",
    app_name="fastapi-app",
    labels={"env": "staging"},
    dynamic_labels={"hostname": lambda: "api-node-1"},
))

@app.get("/ping")
def ping():
    print("Ping received!")
    logger.track_event("ping", {"status": "ok"})
    return {"message": "pong"}
```

---

## 🐍 Example with Synchronous Script

```python
from loki_console_logger_python import LokiLogger
from loki_console_logger_python.config import LokiLoggerOptions

logger = LokiLogger(LokiLoggerOptions(
    url="https://loki.elvenobservability.com/loki/api/v1/push",
    tenant_id="elven",
    app_name="data-script",
    labels={"env": "batch"},
))

print("Running ETL script...")

try:
    raise ValueError("Unexpected value")
except Exception:
    pass

logger.track_event("script_end", {"status": "completed"})

# Optional: force flush for long-running tasks
logger.flush_sync()
```

---

## ⚙️ Configuration Options

| Option | Description | Default |
| --- | --- | --- |
| `url` | Full Loki Push API URL | — |
| `tenant_id` | Value for `X-Scope-OrgID` (multi-tenancy) | — |
| `app_name` | Used as a `label` in logs | — |
| `auth_token` | Optional Bearer token | `None` |
| `batch_size` | Max logs before flush | `10` |
| `flush_interval` | Seconds between auto-flush | `2` |
| `labels` | Fixed labels (e.g., env, service) | `{}` |
| `dynamic_labels` | Runtime-evaluated labels (e.g., hostname) | `{}` |

---

## 🤝 Contributing

Contributions are very welcome — new features, bug fixes, or ideas.

Let's make observability in Python awesome together! 🛠️

1. Fork the repository
2. Create a new branch (`git checkout -b feat/my-feature`)
3. Open a pull request

---

## 📄 License

Licensed under the MIT License.

Created with ❤️ by [Leonardo Zwirtes](https://elven.works/)