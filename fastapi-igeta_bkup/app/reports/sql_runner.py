from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


_PARAM_RE = re.compile(r"(?<!:):([a-zA-Z_][a-zA-Z0-9_]*)")


def strip_sql_comments(sql: str) -> str:
    """
    SQLAlchemy text() は SQL コメント内の `:param` も bind parameter として解釈してしまうため、
    実行前にコメントを除去する。
    """
    # remove block comments
    sql = re.sub(r"/\*[\s\S]*?\*/", "", sql)
    # remove line comments
    sql = re.sub(r"--[^\n]*", "", sql)
    return sql


def extract_named_params(sql: str) -> set[str]:
    """
    SQLAlchemy の text() で使う named parameter (":name") を抽出する。
    ※ "::date" のような Postgres cast は除外する（負の後読みで対応）。
    """
    return set(_PARAM_RE.findall(sql))


@dataclass(frozen=True)
class SqlFileReport:
    report_id: str
    title: str
    sql_path: Path


def load_sql(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    return strip_sql_comments(raw)


def run_sql_report(session: Session, *, sql: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    needed = extract_named_params(sql)
    bind_params = {k: v for k, v in params.items() if k in needed}
    result = session.execute(text(sql), bind_params)
    return [dict(row) for row in result.mappings().all()]

