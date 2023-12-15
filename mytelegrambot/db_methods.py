from typing import Any

from db_connection import connection


def insert(table: str, columns: str, values: str):
    query = f"INSERT INTO {table}({columns})"
    query += f"VALUES ({''.join([f'{i}' for i in values.split(',')])})"
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def select(table: str, columns: str, user: str) -> tuple[tuple[Any, ...], ...]:
    query = f"SELECT {columns} FROM {table} WHERE fk={user}"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows
