from __future__ import annotations

import contextvars
import logging
import os
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, Optional


request_id_ctx_var: Final[contextvars.ContextVar[Optional[str]]] = contextvars.ContextVar(
    "request_id", default=None
)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        record.request_id = request_id_ctx_var.get() or "-"  # type: ignore[attr-defined]
        return True


class _DailyFileRouterHandler(logging.Handler):
    """
    1日単位で出力先ファイルを切り替えるハンドラ。
    出力先: {base_dir}/{YYYY}/{MM}/{prefix}_{YYYY-MM-DD}.log
    """

    def __init__(
        self,
        *,
        base_dir: Path,
        filename_prefix: str,
        level: int = logging.NOTSET,
        encoding: str = "utf-8",
        use_utc: bool = False,
    ) -> None:
        super().__init__(level=level)
        self._base_dir = base_dir
        self._filename_prefix = filename_prefix
        self._encoding = encoding
        self._use_utc = use_utc

        self._lock = threading.RLock()
        self._current_key: str | None = None
        self._file_handler: logging.FileHandler | None = None

    def _now(self, created: float) -> datetime:
        dt = datetime.fromtimestamp(created, tz=timezone.utc if self._use_utc else None)
        return dt

    def _key_for(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d")

    def _path_for(self, dt: datetime) -> Path:
        year = dt.strftime("%Y")
        month = dt.strftime("%m")
        day = dt.strftime("%Y-%m-%d")
        folder = self._base_dir / year / month
        return folder / f"{self._filename_prefix}_{day}.log"

    def _ensure_handler(self, record: logging.LogRecord) -> logging.FileHandler:
        dt = self._now(record.created)
        key = self._key_for(dt)

        if self._file_handler is not None and self._current_key == key:
            return self._file_handler

        path = self._path_for(dt)
        path.parent.mkdir(parents=True, exist_ok=True)

        if self._file_handler is not None:
            try:
                self._file_handler.close()
            finally:
                self._file_handler = None

        fh = logging.FileHandler(path, encoding=self._encoding)
        fh.setLevel(self.level)
        if self.formatter is not None:
            fh.setFormatter(self.formatter)
        for f in self.filters:
            fh.addFilter(f)

        self._file_handler = fh
        self._current_key = key
        return fh

    def emit(self, record: logging.LogRecord) -> None:
        with self._lock:
            handler = self._ensure_handler(record)
            handler.emit(record)

    def close(self) -> None:
        with self._lock:
            if self._file_handler is not None:
                try:
                    self._file_handler.close()
                finally:
                    self._file_handler = None
            super().close()


@dataclass(frozen=True)
class LoggingSettings:
    app_name: str = "fastapi-igeta"
    env: str = "dev"  # dev / prod 想定
    log_level: str = "INFO"
    console_level: str = "INFO"
    log_dir: Path = Path("logs")
    use_utc: bool = False

    @staticmethod
    def from_env() -> "LoggingSettings":
        def _bool(value: str | None, default: bool) -> bool:
            if value is None:
                return default
            return value.strip().lower() in {"1", "true", "yes", "y", "on"}

        return LoggingSettings(
            app_name=os.getenv("APP_NAME", "fastapi-igeta"),
            env=os.getenv("APP_ENV", os.getenv("ENV", "dev")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            console_level=os.getenv("CONSOLE_LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO")),
            log_dir=Path(os.getenv("LOG_DIR", "logs")),
            use_utc=_bool(os.getenv("LOG_USE_UTC"), False),
        )


def configure_logging(settings: LoggingSettings | None = None) -> None:
    settings = settings or LoggingSettings.from_env()

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.DEBUG)  # 各Handler側で制御

    request_id_filter = RequestIdFilter()

    fmt = (
        "%(asctime)s.%(msecs)03d "
        "%(levelname)s "
        "%(name)s "
        "rid=%(request_id)s "
        "%(message)s"
    )
    formatter = logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, settings.console_level.upper(), logging.INFO))
    ch.setFormatter(formatter)
    ch.addFilter(request_id_filter)
    root.addHandler(ch)

    # Daily file (all)
    app_prefix = f"{settings.app_name}"
    fh_all = _DailyFileRouterHandler(
        base_dir=settings.log_dir,
        filename_prefix=app_prefix,
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        use_utc=settings.use_utc,
    )
    fh_all.setFormatter(formatter)
    fh_all.addFilter(request_id_filter)
    root.addHandler(fh_all)

    # Daily file (error+)
    fh_err = _DailyFileRouterHandler(
        base_dir=settings.log_dir,
        filename_prefix=f"{app_prefix}_error",
        level=logging.ERROR,
        use_utc=settings.use_utc,
    )
    fh_err.setFormatter(formatter)
    fh_err.addFilter(request_id_filter)
    root.addHandler(fh_err)

    # Uvicorn/FastAPIのロガーもrootへ流す（ファイル出力対象にする）
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        lg = logging.getLogger(name)
        lg.handlers.clear()
        lg.propagate = True

