from __future__ import annotations

import typing
from . import env

if typing.TYPE_CHECKING:
    import polars as pl
    from snowflake.connector import SnowflakeConnection
    from snowflake.connector.cursor import SnowflakeCursor


def query(
    sql: str,
    *,
    cursor: SnowflakeCursor | None = None,
    conn: SnowflakeConnection | None = None,
) -> pl.DataFrame:
    import polars as pl

    if cursor is None:
        cursor = env.get_snowflake_cursor(conn=conn)
    cursor.execute(sql)
    arrow_table = cursor.fetch_arrow_all()  # type: ignore
    return pl.from_arrow(arrow_table)  # type: ignore
