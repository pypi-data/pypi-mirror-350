from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from snowflake.connector import SnowflakeConnection
    from snowflake.connector.cursor import SnowflakeCursor


_default_connector: dict[str, SnowflakeConnection | None] = {'conn': None}


def get_snowflake_credentials() -> dict[str, str | None]:
    import os
    import json

    raw_credentials = os.environ.get('SNOWFLAKE_CREDENTIALS')
    if raw_credentials is None or raw_credentials == '':
        raise Exception(
            'set credentials as a JSON blob in SNOWFLAKE_CREDENTIALS environment variable'
        )
    credentials: dict[str, str | None] = json.loads(raw_credentials)
    return credentials


def get_snowflake_conn(
    *,
    default: bool = True,
    reset: bool = False,
) -> SnowflakeConnection:
    import snowflake.connector

    if default and _default_connector['conn'] is not None and not reset:
        return _default_connector['conn']
    else:
        credentials = get_snowflake_credentials()
        conn = snowflake.connector.connect(**credentials)
        if default:
            _default_connector['conn'] = conn
        return conn


def get_snowflake_cursor(
    conn: SnowflakeConnection | None = None,
) -> SnowflakeCursor:
    if conn is None:
        conn = get_snowflake_conn()
    return conn.cursor()
