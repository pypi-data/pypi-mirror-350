from typing import Any, Callable, Dict, Optional

from opentelemetry.trace import get_current_span


class LokiLoggerOptions:
    def __init__(
        self,
        url: str,
        tenant_id: str,
        app_name: str,
        auth_token: Optional[str] = None,
        batch_size: int = 10,
        flush_interval: int = 2,
        labels: Optional[Dict[str, str]] = None,
        dynamic_labels: Optional[Dict[str, Callable[[], Any]]] = None,
    ):
        self.url = url
        self.tenant_id = tenant_id
        self.app_name = app_name
        self.auth_token = auth_token
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.labels = labels or {}
        
        def default_trace_id():
            span = get_current_span()
            ctx = span.get_span_context() if span else None
            return ctx.trace_id if ctx and ctx.is_valid else 0

        def default_span_id():
            span = get_current_span()
            ctx = span.get_span_context() if span else None
            return ctx.span_id if ctx and ctx.is_valid else 0

        default_labels = {
            "trace_id": lambda: format(default_trace_id(), '032x'),
            "span_id": lambda: format(default_span_id(), '016x'),
        }

        self.dynamic_labels = {**default_labels, **(dynamic_labels or {})}