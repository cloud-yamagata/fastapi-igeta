# ruff: noqa: T201
"""
DB辞書.tsv から app/entities/<table>/model.py, repository.py と
app/routers/<table>.py を生成する（手書きテーブルは --skip で除外）。

使用例（fastapi-igeta 直下）::
    python scripts/gen_entities_from_tsv.py --tsv D:/DB辞書.tsv
"""
from __future__ import annotations

import argparse
import csv
import io
from collections import OrderedDict
from decimal import Decimal
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
ENTITIES = ROOT / "app" / "entities"
ROUTERS = ROOT / "app" / "routers"
# プロジェクト直下に DB辞書.tsv が無い場合の参照元（再現用コピー元）
FALLBACK_TSV = Path(r"d:\DB辞書.tsv")


def unquote(s: str) -> str:
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace('""', '"')
    return s


def table_to_class(table: str) -> str:
    return "".join(p[:1].upper() + p[1:] if p else "" for p in table.split("_"))


def col_to_py(col: str) -> str:
    if col in ("class", "def", "from", "import", "return", "None", "True", "False", "global"):
        return col + "_"
    return col


def type_spec(dtype: str, maxlen: str, scale: str) -> tuple[str, str, str]:
    """(sqlalchemy_import_symbol, type_expr_for_mapped_column, tail_comment)"""
    d = (dtype or "").strip().lower()
    if not d:
        return "JSONB", "JSONB", " | #(辞書:型セル空→jsonb)"

    if d in ("varchar", "character varying"):
        return "Text", "Text()", ""
    if d == "text":
        return "Text", "Text()", ""
    if d == "char":
        ln = maxlen.strip()
        n = int(ln) if ln.isdigit() else 1
        return "String", f"String({n})", ""
    if d in ("int", "integer"):
        return "Integer", "Integer()", ""
    if d == "smallint":
        return "SmallInteger", "SmallInteger()", ""
    if d in ("bool", "boolean"):
        return "Boolean", "Boolean()", ""
    if d == "date":
        return "Date", "Date()", ""
    if d == "time":
        return "Time", "Time()", ""
    if d == "timestamp":
        return "DateTime", "DateTime(timezone=False)", ""
    if d == "numeric":
        p = maxlen.strip()
        s = scale.strip()
        pi = int(p) if p.isdigit() else 18
        si = int(s) if s.isdigit() else 0
        return "Numeric", f"Numeric({pi}, {si})", ""
    if d in ("jsonb", "json"):
        return "JSONB", "JSONB", ""

    return "Text", "Text()", f" | #(辞書型:{d}→text扱い)"


def mapped_py_type(imp: str, nullable: bool) -> str:
    base: str
    if imp == "DateTime":
        base = "datetime.datetime"
    elif imp == "Date":
        base = "datetime.date"
    elif imp == "Time":
        base = "datetime.time"
    elif imp == "Numeric":
        base = "Decimal"
    elif imp == "JSONB":
        base = "Any"
    elif imp in ("Integer", "SmallInteger"):
        base = "int"
    elif imp == "Boolean":
        base = "bool"
    else:
        base = "str"
    if nullable:
        return f"{base} | None"
    return base


def _parse_tsv_rows(reader: Iterator[list[str]]) -> OrderedDict[str, dict]:
    tables: OrderedDict[str, dict] = OrderedDict()
    next(reader, None)
    for row in reader:
        if len(row) < 11:
            continue
        tname = unquote(row[0])
        tcomment = unquote(row[1])
        cname = unquote(row[3])
        ccomment = unquote(row[4])
        dtype = unquote(row[5])
        maxlen = unquote(row[6]) if len(row) > 6 else ""
        scale = unquote(row[7]) if len(row) > 7 else ""
        is_pk = unquote(row[8]) == "1"
        is_null = unquote(row[10]).lower() if len(row) > 10 else ""
        not_null = is_null == "not null"

        if tname not in tables:
            tables[tname] = {"comment": tcomment, "cols": []}
        tables[tname]["cols"].append(
            {
                "name": cname,
                "comment": ccomment,
                "dtype": dtype,
                "maxlen": maxlen,
                "scale": scale,
                "pk": is_pk,
                "not_null": not_null,
            }
        )
    return tables


def parse_tsv(path: Path) -> OrderedDict[str, dict]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        return _parse_tsv_rows(reader)


def parse_tsv_string(text: str) -> OrderedDict[str, dict]:
    reader = csv.reader(io.StringIO(text), delimiter="\t")
    return _parse_tsv_rows(reader)


def build_model(table: str, meta: dict) -> str:
    cls = table_to_class(table)
    tcom = meta["comment"]

    sa_imports: set[str] = set()
    pg_jsonb = False
    col_lines: list[str] = []

    for c in meta["cols"]:
        cname = c["name"]
        pyname = col_to_py(cname)
        lbl = c["comment"] or "#(論理名なし・DB辞書列コメント空)"
        pk_tag = "PK" if c["pk"] else ""
        null_tag = "NOT NULL" if c["not_null"] else "NULL可"
        imp, type_expr, extra = type_spec(c["dtype"], c["maxlen"], c["scale"])
        if imp == "JSONB":
            pg_jsonb = True
        else:
            sa_imports.add(imp)

        ann = mapped_py_type(imp, not c["not_null"])
        pk_kw = ", primary_key=True" if c["pk"] else ""
        null_kw = "" if c["not_null"] else ", nullable=True"

        if pyname != cname:
            mc = f'mapped_column("{cname}", {type_expr}{pk_kw}{null_kw})'
        else:
            mc = f"mapped_column({type_expr}{pk_kw}{null_kw})"

        col_lines.append(
            f"    {pyname}: Mapped[{ann}] = {mc}  # {cname} | {lbl} | {pk_tag} | {null_tag}{extra}"
        )

    import_lines = ["import datetime", "from decimal import Decimal", "from typing import Any", ""]
    if sa_imports:
        syms = ", ".join(sorted(sa_imports))
        import_lines.append(f"from sqlalchemy import {syms}")
    if pg_jsonb:
        import_lines.append("from sqlalchemy.dialects.postgresql import JSONB")
    import_lines.extend(["from sqlalchemy.orm import Mapped, mapped_column", "", "from app.db.base import Base", ""])

    body = [
        '"""',
        f"テーブル ``{table}`` の SQLAlchemy モデル（DB辞書.tsv 自動生成）。",
        '"""',
        "from __future__ import annotations",
        "",
        *import_lines,
        "",
        f"class {cls}(Base):",
        f'    """{tcom}"""',
        "",
        f"    # table: {table} | {tcom}",
        f'    __tablename__ = "{table}"',
        "",
        *col_lines,
        "",
    ]
    return "\n".join(body)


def build_repository(table: str, meta: dict) -> str:
    cls = table_to_class(table)
    repo_cls = f"{cls}Repository"
    pk_cols = [(col_to_py(c["name"]), c["name"]) for c in meta["cols"] if c["pk"]]

    if len(pk_cols) == 0:
        get_block = f"""
    @staticmethod
    def get_first(session: Session) -> {cls} | None:
        return session.scalars(select({cls})).first()
"""
        del_block = f"""
    @staticmethod
    def delete_first(session: Session) -> bool:
        row = {repo_cls}.get_first(session)
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True
"""
    elif len(pk_cols) == 1:
        py, _db = pk_cols[0]
        get_block = f"""
    @staticmethod
    def get_by_pk(session: Session, {py}: object) -> {cls} | None:
        return session.get({cls}, {py})
"""
        del_block = f"""
    @staticmethod
    def delete_by_pk(session: Session, {py}: object) -> bool:
        row = session.get({cls}, {py})
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True
"""
    else:
        args = ", ".join(f"{py}: object" for py, _ in pk_cols)
        where = " & ".join(f"({cls}.{py} == {py})" for py, _ in pk_cols)
        vals = ", ".join(py for py, _ in pk_cols)
        get_block = f"""
    @staticmethod
    def get_by_pk(session: Session, {args}) -> {cls} | None:
        stmt = select({cls}).where({where})
        return session.scalars(stmt).first()
"""
        del_block = f"""
    @staticmethod
    def delete_by_pk(session: Session, {args}) -> bool:
        row = {repo_cls}.get_by_pk(session, {vals})
        if row is None:
            return False
        session.delete(row)
        session.commit()
        return True
"""

    return f'''"""{table} 永続化アクセス（CRUD 雛形・自動生成）。"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.{table}.model import {cls}


class {repo_cls}:
    @staticmethod
    def list_all(session: Session) -> list[{cls}]:
        return list(session.scalars(select({cls})).all())
{get_block}
    @staticmethod
    def create(session: Session, row: {cls}) -> {cls}:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @staticmethod
    def update(session: Session, row: {cls}) -> {cls}:
        session.add(row)
        session.commit()
        session.refresh(row)
        return row
{del_block}
    @staticmethod
    def delete_entity(session: Session, row: {cls}) -> None:
        session.delete(row)
        session.commit()
'''


def build_router(table: str, meta: dict) -> str:
    cls = table_to_class(table)
    repo = f"{cls}Repository"
    path = f"/{table}/"

    return f'''"""{table} API 雛形（dict 応答・専用スキーマは後から分離可）。"""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_session
from app.entities.{table}.model import {cls}
from app.entities.{table}.repository import {repo}

router = APIRouter(tags=["{table}"])


def _cell(v: object) -> object:
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


@router.get("{path}", response_model=list[dict])
def list_{table}(session: Session = Depends(get_session)) -> list[dict]:
    rows = {repo}.list_all(session)
    keys = [c.key for c in {cls}.__table__.columns]
    return [{{k: _cell(getattr(r, k)) for k in keys}} for r in rows]
'''


def write_generated(tables: OrderedDict[str, dict], skip: set[str]) -> int:
    n = 0
    for table, meta in tables.items():
        if table in skip:
            continue
        d = ENTITIES / table
        d.mkdir(parents=True, exist_ok=True)
        (d / "__init__.py").write_text(f'"""entity: {table} (generated)"""\n', encoding="utf-8")
        (d / "model.py").write_text(build_model(table, meta), encoding="utf-8")
        (d / "repository.py").write_text(build_repository(table, meta), encoding="utf-8")
        (ROUTERS / f"{table}.py").write_text(build_router(table, meta), encoding="utf-8")
        n += 1
    return n


def write_entities_init(tables: OrderedDict[str, dict]) -> None:
    lines = [
        '"""ORM 全テーブル集約（DB辞書と対応）。Alembic / メタデータ用。"""',
        "from __future__ import annotations",
        "",
    ]
    exports: list[str] = []
    for table in tables:
        cls = table_to_class(table)
        lines.append(f"from app.entities.{table}.model import {cls}")
        exports.append(cls)
    lines.append("")
    lines.append("__all__ = [")
    for e in exports:
        lines.append(f'    "{e}",')
    lines.append("]")
    lines.append("")
    (ENTITIES / "__init__.py").write_text("\n".join(lines), encoding="utf-8")


def resolve_tsv_path(explicit: Path | None) -> Path:
    """優先: 引数 → プロジェクト直下 DB辞書.tsv → d:\\DB辞書.tsv"""
    if explicit is not None:
        if not explicit.is_file():
            raise FileNotFoundError(str(explicit))
        return explicit
    local = ROOT / "DB辞書.tsv"
    if local.is_file():
        return local
    if FALLBACK_TSV.is_file():
        return FALLBACK_TSV
    raise FileNotFoundError(
        f"DB辞書.tsv が見つかりません（{local} または {FALLBACK_TSV} を配置してください）"
    )


def run_codegen(tsv: Path | None = None) -> tuple[int, OrderedDict[str, dict]]:
    path = resolve_tsv_path(tsv)
    tables = parse_tsv(path)
    handcrafted = {"te_material", "tr_item", "tr_constant", "te_monthly_plan"}
    n = write_generated(tables, skip=handcrafted)
    write_entities_init(tables)
    print(f"Wrote {n} generated entity sets; preserved handcrafted {sorted(handcrafted)}")
    print("Updated app/entities/__init__.py — merge main.py imports from fragment or template")
    return n, tables


def main() -> None:
    ap = argparse.ArgumentParser()
    default_tsv = ROOT / "DB辞書.tsv"
    has_default = default_tsv.is_file() or FALLBACK_TSV.is_file()
    ap.add_argument(
        "--tsv",
        type=Path,
        default=None,
        required=not has_default,
        nargs="?",
        help=f"DB辞書.tsv（未指定時: {default_tsv.name} または {FALLBACK_TSV}）",
    )
    args = ap.parse_args()
    run_codegen(args.tsv)


if __name__ == "__main__":
    main()
