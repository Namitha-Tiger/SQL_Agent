import pytest

from src.safety import validate_sql


def test_valid_select():
    sql = "SELECT * FROM customers;"
    assert validate_sql(sql) == "SELECT * FROM customers"


def test_reject_insert():
    with pytest.raises(ValueError):
        validate_sql(
            "INSERT INTO customers VALUES (1)"
        )


def test_reject_update():
    with pytest.raises(ValueError):
        validate_sql(
            "UPDATE customers SET city='Hyd'"
        )


def test_reject_delete():
    with pytest.raises(ValueError):
        validate_sql(
            "DELETE FROM customers"
        )


def test_reject_drop():
    with pytest.raises(ValueError):
        validate_sql(
            "DROP TABLE customers"
        )


def test_reject_multiple_statements():
    with pytest.raises(ValueError):
        validate_sql(
            "SELECT * FROM customers; DROP TABLE customers;"
        )


def test_reject_comments():
    with pytest.raises(ValueError):
        validate_sql(
            "SELECT * FROM customers -- test"
        )