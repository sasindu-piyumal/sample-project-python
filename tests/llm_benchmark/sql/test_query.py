import sqlite3

import pytest

from llm_benchmark.sql import query
from llm_benchmark.sql.query import SqlQuery


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Presence", True),
        ("Roundabout", False),
    ],
)
def test_query_album(name: str, expected: bool) -> None:
    assert SqlQuery.query_album(name) == expected


def test_database_connection_rejects_writes(tmp_path, monkeypatch) -> None:
    database = tmp_path / "albums.db"
    with sqlite3.connect(database) as conn:
        conn.execute("CREATE TABLE Album (Title TEXT)")
        conn.execute("INSERT INTO Album VALUES ('Presence')")

    monkeypatch.setattr(query, "_DB_PATH", database)

    assert SqlQuery.query_album("Presence") is True
    with pytest.raises(sqlite3.OperationalError, match="readonly"):
        with query._connect() as conn:
            conn.execute("DELETE FROM Album")

    with sqlite3.connect(database) as conn:
        assert conn.execute("SELECT COUNT(*) FROM Album").fetchone() == (1,)


def test_benchmark_query_album(benchmark) -> None:
    benchmark(SqlQuery.query_album, "Presence")


def test_join_albums() -> None:
    assert SqlQuery.join_albums()[0] == (
        "For Those About To Rock (We Salute You)",
        "For Those About To Rock We Salute You",
        "AC/DC",
    )


def test_benchmark_join_albums(benchmark) -> None:
    benchmark(SqlQuery.join_albums)


def test_top_invoices() -> None:
    top = SqlQuery.top_invoices()
    assert top[0][2] == 25.86
    assert top[2][2] == 21.86
    assert len(top) == 10


def test_benchmark_top_invoices(benchmark) -> None:
    benchmark(SqlQuery.top_invoices)
