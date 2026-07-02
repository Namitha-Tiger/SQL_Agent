from unittest.mock import MagicMock

from src.sql_tools import execute_select
from src.sql_tools import check_connection


def test_execute_select_returns_rows():

    fake_cursor = MagicMock()

    fake_cursor.fetchall.return_value = [
        {
            "customer_id": 1,
            "city": "Hyderabad",
        }
    ]

    fake_connection = MagicMock()

    fake_connection.cursor.return_value = fake_cursor

    rows = execute_select(
        "SELECT * FROM customers",
        fake_connection,
    )

    assert len(rows) == 1
    assert rows[0]["city"] == "Hyderabad"

    fake_cursor.execute.assert_called_once_with(
        "SELECT * FROM customers"
    )

    fake_cursor.close.assert_called_once()


def test_check_connection_success():

    fake_cursor = MagicMock()

    fake_connection = MagicMock()

    fake_connection.cursor.return_value = fake_cursor

    assert check_connection(fake_connection) is True

    fake_cursor.execute.assert_called_once_with("SELECT 1")
    fake_cursor.close.assert_called_once()