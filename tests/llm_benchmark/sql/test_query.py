import pytest

from llm_benchmark.sql.query import SqlQuery


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Presence", True),
        ("Roundabout", False),
    ],
)
def test_query_album(name: str, expected: bool, isolated_sql_query) -> None:
    assert SqlQuery.query_album(name) == expected


def test_benchmark_query_album(benchmark, isolated_sql_query) -> None:
    benchmark(SqlQuery.query_album, "Presence")


def test_join_albums(isolated_sql_query) -> None:
    assert SqlQuery.join_albums()[0] == (
        "For Those About To Rock (We Salute You)",
        "For Those About To Rock We Salute You",
        "AC/DC",
    )


def test_benchmark_join_albums(benchmark, isolated_sql_query) -> None:
    benchmark(SqlQuery.join_albums)


def test_top_invoices(isolated_sql_query) -> None:
    top = SqlQuery.top_invoices()
    assert top[0][2] == 25.86
    assert top[2][2] == 21.86
    assert len(top) == 10


def test_benchmark_top_invoices(benchmark, isolated_sql_query) -> None:
    benchmark(SqlQuery.top_invoices)
