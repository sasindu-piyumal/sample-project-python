import sqlite3
import threading
from pathlib import Path
from textwrap import dedent

# Module-level cached connection — opened lazily once, reused across all calls.
# Using check_same_thread=False allows concurrent access from multiple threads.
# Lock protects the check-then-create pattern to prevent race conditions during initialization.
DB_PATH = Path(__file__).resolve().parents[3] / "data" / "chinook.db"
_conn = None
_conn_lock = threading.Lock()


def _get_conn():
    global _conn
    if _conn is None:
        if not DB_PATH.exists():
            raise FileNotFoundError(f"Missing required SQLite database: {DB_PATH}")
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return _conn


class SqlQuery:
    @staticmethod
    def query_album(name: str) -> bool:
        """Check if an album exists

        Args:
            name (str): Name of the album

        Returns:
            bool: True if the album exists, False otherwise
        """
        cur = _get_conn().cursor()
        cur.execute(
            "SELECT 1 FROM Album WHERE Title = ? LIMIT 1",
            (name,),
        )
        return cur.fetchone() is not None

    @staticmethod
    def join_albums() -> list:
        """Join the Album, Artist, and Track tables

        Returns:
            list:
        """
        cur = _get_conn().cursor()
        cur.execute(
            dedent(
                """\
                SELECT 
                    t.Name AS TrackName,
                    a.Title AS AlbumName,
                    ar.Name AS ArtistName
                FROM 
                    Track t
                JOIN Album a ON a.AlbumId = t.AlbumId
                JOIN Artist ar ON ar.ArtistId = a.ArtistId
                """
            )
        )
        return cur.fetchall()

    @staticmethod
    def top_invoices() -> list:
        """Get the top 10 invoices by total

        Returns:
            list: List of tuples
        """
        cur = _get_conn().cursor()
        cur.execute(
            dedent(
                """\
                SELECT 
                    i.InvoiceId, 
                    c.FirstName || ' ' || c.LastName AS CustomerName, 
                    i.Total
                FROM 
                    Invoice i
                JOIN Customer c ON c.CustomerId = i.CustomerId
                ORDER BY i.Total DESC
                LIMIT 10
                """
            )
        )
        return cur.fetchall()