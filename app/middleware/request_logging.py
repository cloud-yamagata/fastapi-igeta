from __future__ import annotations

import logging
import time
import uuid
from typing import Callable, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.logging_config import request_id_ctx_var


logger = logging.getLogger("app.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        request_id_header: str = "X-Request-ID",
        log_request_body: bool = False,
        max_body_length: int = 2048,
    ) -> None:
        super().__init__(app)
        self._request_id_header = request_id_header
        self._log_request_body = log_request_body
        self._max_body_length = max_body_length

    def _get_request_id(self, request: Request) -> str:
        rid = request.headers.get(self._request_id_header)
        if rid and rid.strip():
            return rid.strip()
        return uuid.uuid4().hex

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        rid = self._get_request_id(request)
        token = request_id_ctx_var.set(rid)
        start = time.perf_counter()

        body_preview: Optional[str] = None
        if self._log_request_body:
            try:
                raw = await request.body()
                if raw:
                    body_preview = raw[: self._max_body_length].decode(
                        "utf-8", errors="replace"
                    )
            except Exception:
                body_preview = "<unavailable>"

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000.0
            logger.exception(
                "request_failed method=%s path=%s query=%s client=%s ua=%s duration_ms=%.2f body=%s",
                request.method,
                request.url.path,
                request.url.query,
                getattr(request.client, "host", "-"),
                request.headers.get("user-agent", "-"),
                duration_ms,
                body_preview if body_preview is not None else "-",
            )
            raise
        finally:
            request_id_ctx_var.reset(token)

        duration_ms = (time.perf_counter() - start) * 1000.0
        logger.info(
            "request_completed method=%s path=%s query=%s status=%s client=%s ua=%s duration_ms=%.2f body=%s",
            request.method,
            request.url.path,
            request.url.query,
            getattr(response, "status_code", "-"),
            getattr(request.client, "host", "-"),
            request.headers.get("user-agent", "-"),
            duration_ms,
            body_preview if body_preview is not None else "-",
        )

        response.headers[self._request_id_header] = rid
        return response

