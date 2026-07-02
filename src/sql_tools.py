from typing import Any

import mysql.connector
from mysql.connector import MySQLConnection

from .config import get_settings


def create_connection() -> MySQLConnection:
    """
    Create and return a MySQL connection using values
    from config.py.
    """

    settings = get_settings()

    return mysql.connector.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
    )


def execute_select(
    sql: str,
    connection: MySQLConnection,
) -> list[dict[str, Any]]:
    """
    Execute a SELECT statement and return rows as a list
    of dictionaries.
    """

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(sql)

        rows = cursor.fetchall()

        return list(rows)

    finally:
        cursor.close()


def check_connection(connection: MySQLConnection) -> bool:
    """
    Returns True if the connection is alive.
    """

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return True
    except Exception:
        return False
