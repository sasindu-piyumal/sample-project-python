from unittest.mock import patch

import pytest

try:
    import main
except PermissionError:
    main = None


pytestmark = pytest.mark.skipif(main is None, reason="Unable to initialize main logging")


def test_sql_handles_empty_join_albums(capsys) -> None:
    with (
        patch.object(main.SqlQuery, "query_album", return_value=False),
        patch.object(main.SqlQuery, "join_albums", return_value=[]),
        patch.object(main.SqlQuery, "top_invoices", return_value=[]),
    ):
        main.sql()

    assert "join_albums()\n\n" in capsys.readouterr().out


def test_sql_prints_first_joined_album(capsys) -> None:
    album = ("Track", "Album", "Artist")
    with (
        patch.object(main.SqlQuery, "query_album", return_value=False),
        patch.object(main.SqlQuery, "join_albums", return_value=[album]),
        patch.object(main.SqlQuery, "top_invoices", return_value=[]),
    ):
        main.sql()

    assert "join_albums()\n('Track', 'Album', 'Artist')\n" in capsys.readouterr().out
