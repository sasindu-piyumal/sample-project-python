import pytest

from llm_benchmark.sql.query import SqlQuery


class TestAlbumLookup:
    """Tests for album lookup correctness."""

    def test_query_album_exact_match_true(self, isolated_sql_query) -> None:
        """Album lookup returns true for exact album title match."""
        assert SqlQuery.query_album("Presence") is True

    def test_query_album_absent_false(self, isolated_sql_query) -> None:
        """Album lookup returns false for album not in database."""
        assert SqlQuery.query_album("Roundabout") is False

    def test_query_album_non_exact_match_false(self, isolated_sql_query) -> None:
        """Album lookup returns false for partial or case-mismatched name."""
        assert SqlQuery.query_album("presence") is False

    def test_query_album_partial_name_false(self, isolated_sql_query) -> None:
        """Album lookup returns false for partial album name."""
        assert SqlQuery.query_album("Presence (partial)") is False

    def test_query_album_existing_album_true(self, isolated_sql_query) -> None:
        """Album lookup returns true for another existing album."""
        assert SqlQuery.query_album("For Those About To Rock We Salute You") is True

    def test_query_album_empty_string_false(self, isolated_sql_query) -> None:
        """Album lookup returns false for empty string."""
        assert SqlQuery.query_album("") is False

    def test_query_album_whitespace_only_false(self, isolated_sql_query) -> None:
        """Album lookup returns false for whitespace-only string."""
        assert SqlQuery.query_album("   ") is False


class TestAlbumArtistTrackJoins:
    """Tests for album, artist, and track join operations."""

    def test_join_albums_returns_list(self, isolated_sql_query) -> None:
        """Join albums returns a list."""
        result = SqlQuery.join_albums()
        assert isinstance(result, list)

    def test_join_albums_first_result_exact(self, isolated_sql_query) -> None:
        """First join result contains expected track, album, and artist."""
        result = SqlQuery.join_albums()
        assert len(result) > 0
        assert result[0] == (
            "For Those About To Rock (We Salute You)",
            "For Those About To Rock We Salute You",
            "AC/DC",
        )

    def test_join_albums_contains_expected_entries(self, isolated_sql_query) -> None:
        """Join result contains all expected track-album-artist tuples."""
        result = SqlQuery.join_albums()
        
        # Verify we have all three expected tracks
        assert len(result) >= 3
        
        # Check all expected tuples are present
        expected_tuples = [
            ("For Those About To Rock (We Salute You)", "For Those About To Rock We Salute You", "AC/DC"),
            ("Rock and Roll", "Presence", "Led Zeppelin"),
            ("In the Flesh?", "The Wall", "Pink Floyd"),
        ]
        
        for expected_tuple in expected_tuples:
            assert expected_tuple in result

    def test_join_albums_tuple_structure(self, isolated_sql_query) -> None:
        """Each join result tuple has three elements: track, album, artist."""
        result = SqlQuery.join_albums()
        
        for row in result:
            assert len(row) == 3
            track_name, album_name, artist_name = row
            assert isinstance(track_name, str)
            assert isinstance(album_name, str)
            assert isinstance(artist_name, str)

    def test_join_albums_no_empty_fields(self, isolated_sql_query) -> None:
        """Join results have no empty or None fields."""
        result = SqlQuery.join_albums()
        
        for row in result:
            assert row[0]  # Track name not empty
            assert row[1]  # Album name not empty
            assert row[2]  # Artist name not empty


class TestTopInvoices:
    """Tests for top invoices query."""

    def test_top_invoices_returns_list(self, isolated_sql_query) -> None:
        """Top invoices returns a list."""
        result = SqlQuery.top_invoices()
        assert isinstance(result, list)

    def test_top_invoices_limit_ten(self, isolated_sql_query) -> None:
        """Top invoices returns at most 10 rows."""
        result = SqlQuery.top_invoices()
        assert len(result) <= 10

    def test_top_invoices_exactly_ten(self, isolated_sql_query) -> None:
        """Top invoices returns exactly 10 rows with 10+ invoices in database."""
        result = SqlQuery.top_invoices()
        assert len(result) == 10

    def test_top_invoices_tuple_structure(self, isolated_sql_query) -> None:
        """Each invoice tuple has three elements: id, customer name, total."""
        result = SqlQuery.top_invoices()
        
        for row in result:
            assert len(row) == 3
            invoice_id, customer_name, total = row
            assert isinstance(invoice_id, int)
            assert isinstance(customer_name, str)
            assert isinstance(total, (int, float))

    def test_top_invoices_first_total_exact(self, isolated_sql_query) -> None:
        """First invoice has exact expected total."""
        result = SqlQuery.top_invoices()
        assert result[0][2] == 25.86

    def test_top_invoices_third_total_exact(self, isolated_sql_query) -> None:
        """Third invoice has exact expected total."""
        result = SqlQuery.top_invoices()
        assert result[2][2] == 21.86

    def test_top_invoices_descending_order(self, isolated_sql_query) -> None:
        """Invoices are ordered by total in descending order."""
        result = SqlQuery.top_invoices()
        
        for i in range(len(result) - 1):
            assert result[i][2] >= result[i + 1][2]

    def test_top_invoices_strict_descending(self, isolated_sql_query) -> None:
        """Invoices are in strictly descending order by total."""
        result = SqlQuery.top_invoices()
        
        for i in range(len(result) - 1):
            assert result[i][2] > result[i + 1][2]

    def test_top_invoices_customer_names_format(self, isolated_sql_query) -> None:
        """Customer names are formatted as 'FirstName LastName'."""
        result = SqlQuery.top_invoices()
        
        for row in result:
            customer_name = row[1]
            # Name should contain at least one space (first and last name)
            assert " " in customer_name

    def test_top_invoices_no_empty_customer_names(self, isolated_sql_query) -> None:
        """No invoice has an empty customer name."""
        result = SqlQuery.top_invoices()
        
        for row in result:
            assert row[1]  # Customer name not empty
            assert row[1].strip()  # Customer name not just whitespace

    def test_top_invoices_positive_totals(self, isolated_sql_query) -> None:
        """All invoice totals are positive."""
        result = SqlQuery.top_invoices()
        
        for row in result:
            assert row[2] > 0

    def test_top_invoices_first_customer_john_doe(self, isolated_sql_query) -> None:
        """First invoice customer is John Doe."""
        result = SqlQuery.top_invoices()
        assert result[0][1] == "John Doe"


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
