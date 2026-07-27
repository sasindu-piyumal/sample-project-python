import sqlite3

import pytest

from llm_benchmark.sql.query import DB_PATH, SqlQuery


def _has_chinook_db() -> bool:
    if not DB_PATH.exists():
        return False
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute("SELECT 1 FROM Album LIMIT 1")
        finally:
            conn.close()
    except sqlite3.Error:
        return False
    return True


pytestmark = pytest.mark.skipif(
    not _has_chinook_db(), reason=f"Missing required SQLite database: {DB_PATH}"
)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Presence", True),
        ("Roundabout", False),
    ],
)
def test_query_album(name: str, expected: bool) -> None:
    assert SqlQuery.query_album(name) == expected


def test_join_albums() -> None:
    assert SqlQuery.join_albums()[0] == (
        "For Those About To Rock (We Salute You)",
        "For Those About To Rock We Salute You",
        "AC/DC",
    )


def test_top_invoices() -> None:
    top = SqlQuery.top_invoices()
    assert top[0][2] == 25.86
    assert top[2][2] == 21.86
    assert len(top) == 10


def test_benchmark_top_invoices(benchmark) -> None:
    benchmark(SqlQuery.top_invoices)
