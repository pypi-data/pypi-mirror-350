import sqlite3
from contextlib import contextmanager
from typing import List, Optional, Tuple, Any
from batem.reno.utils import FilePathBuilder


@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(FilePathBuilder().get_irise_db_path())
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query: str, params: Optional[tuple] = None
                  ) -> List[Tuple[Any, ...]]:
    """Execute a query and return results."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()


def get_table_schema(table_name: str) -> List[Tuple[str, str]]:
    """Get the schema of a table."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        return cursor.fetchall()


def print_table_schema(table_name: str):
    schema = get_table_schema(table_name)
    print(f"{table_name} table schema:")
    for column in schema:
        print(f"Column: {column[1]}, Type: {column[2]}")
