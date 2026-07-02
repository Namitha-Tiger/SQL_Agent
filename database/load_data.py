from __future__ import annotations

import csv
import os
import mysql.connector
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

load_dotenv()

from mysql.connector import Error


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMA_FILE = BASE_DIR / "database" / "mysql_schema.sql"


def get_connection() -> mysql.connector.MySQLConnection:
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "retail_agent_assignment"),
        "autocommit": False,
    }
    return mysql.connector.connect(**config)


def execute_schema(conn: mysql.connector.MySQLConnection) -> None:
    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
    statements = [stmt.strip() for stmt in schema_sql.split(";") if stmt.strip()]
    cursor = conn.cursor()
    try:
        for statement in statements:
            cursor.execute(statement)
        conn.commit()
    finally:
        cursor.close()


def clear_tables(conn: mysql.connector.MySQLConnection) -> None:
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM returns")
        cursor.execute("DELETE FROM sales_transactions")
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM stores")
        conn.commit()
    finally:
        cursor.close()


def read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_table(conn: mysql.connector.MySQLConnection, table_name: str, csv_file: str, columns: list[str]) -> None:
    rows = read_csv_rows(DATA_DIR / csv_file)
    if not rows:
        return

    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    values = []
    for row in rows:
        values.append(tuple(row[col] for col in columns))

    cursor = conn.cursor()
    try:
        cursor.executemany(sql, values)
        conn.commit()
    finally:
        cursor.close()


def main() -> None:
    conn = None
    try:
        conn = get_connection()
        execute_schema(conn)
        clear_tables(conn)

        load_table(conn, "stores", "stores.csv", ["store_id", "store_name", "region", "city", "store_type"])
        load_table(conn, "products", "products.csv", ["product_id", "product_name", "category", "sub_category", "base_price"])
        load_table(conn, "customers", "customers.csv", ["customer_id", "customer_segment", "signup_date", "preferred_channel", "city"])
        load_table(
            conn,
            "sales_transactions",
            "sales_transactions.csv",
            [
                "order_id",
                "order_date",
                "store_id",
                "product_id",
                "customer_id",
                "sales_channel",
                "units_sold",
                "unit_price",
                "discount_pct",
                "payment_status",
                "delivery_status",
            ],
        )
        load_table(conn, "returns", "returns.csv", ["return_id", "order_id", "return_date", "return_reason"])

        print("CSV data loaded successfully into MySQL.")
    except Error as exc:
        print(f"MySQL error: {exc}")
        raise
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
