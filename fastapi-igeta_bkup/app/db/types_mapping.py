"""
DB辞書の型を PostgreSQL / SQLAlchemy / Python に正規化する際のルール（ドキュメント兼用）。

許可される DB 型（辞書・実DB の表記ゆれをここで吸収する想定）:
- 数値: smallint, integer, numeric(p,s)
- 文字列: text, char(n)  … varchar(n) は text または char(n) に寄せる方針でモデル側で決定
- 日付/時刻: date, time, timestamp
- 論理: boolean（辞書の bool も boolean とみなす）
- JSON: jsonb

Python（ORM 属性）の対応目安:
- smallint / integer → int
- numeric → decimal.Decimal（API 層で float 等へ変換可）
- text / char → str
- date / time / timestamp → datetime.*
- boolean → bool
- jsonb → dict | list 等（任意構造は typing.Any）

---

Entity model（model.py）のコメント記載ルール（運用で統一）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python の標準的な行末 ``#`` に加え、クラスには Google スタイルの docstring でテーブル概要を書くと
レビュー・差分把握が容易です（Sphinx / IDE のホバー表示にも向く）。

**推奨パターン**

1. **モジュール先頭** … このファイルの役割（どのテーブルか）を 1～2 行。
2. **クラス docstring** … テーブル論理名（DB辞書 ``table_comment``）、補足があれば Note。
3. **``__tablename__`` 行末** … ``# table: <物理名> | <論理名（table_comment）>``
4. **各カラム定義の行末** … 次のセグメントを ``|`` で区切る::

       # <物理列名> | <論理名（DB辞書 column_comment）> | <PK/FK/索引> | <NULL可否> | <補足>

   - 論理名が DB辞書で **空** のときは ``#(論理名なし)`` と書く。
   - 辞書の型・NULL と実装が異なる場合は **補足** に ``実装: …`` と記す。
   - Javadoc 風にタグを付ける場合の例（任意）::

       # @column material_no  @label 原料NO  @pk

   タグ形式はチームで統一できれば検索しやすい（必須ではない）。

**NULL 可否の表記例**

- ``NOT NULL`` … 辞書上 not null
- ``NULL可`` … 辞書上 nullable または実ORMで nullable=True
- ``#(辞書:未記載)`` … is_nullable が判断しづらい列

"""

from __future__ import annotations

# 将来、TSV 検証スクリプトから参照する定数として拡張可能
NORMALIZED_PG_TYPES = frozenset(
    {
        "smallint",
        "integer",
        "numeric",
        "text",
        "char",
        "date",
        "time",
        "timestamp",
        "boolean",
        "jsonb",
    }
)
