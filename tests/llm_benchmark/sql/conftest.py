"""Pytest fixtures for SQL query tests.

Creates a temporary SQLite database with minimal Album, Artist, Track, Customer,
and Invoice schema with representative records. Redirects the SQL module to use
the temporary database and isolates the module-level connection cache.
"""

import sqlite3
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from llm_benchmark.sql import query as sql_query_module


@pytest.fixture
def temp_db() -> Generator[sqlite3.Connection, None, None]:
    """Create a temporary SQLite database with Chinook schema.
    
    Yields:
        sqlite3.Connection: Connection to the temporary database.
    """
    # Create temporary database file
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db_path = f.name
    
    try:
        conn = sqlite3.connect(temp_db_path)
        
        # Create Artist table
        conn.execute("""
            CREATE TABLE Artist (
                ArtistId INTEGER PRIMARY KEY,
                Name TEXT NOT NULL
            )
        """)
        
        # Create Album table
        conn.execute("""
            CREATE TABLE Album (
                AlbumId INTEGER PRIMARY KEY,
                Title TEXT NOT NULL,
                ArtistId INTEGER NOT NULL,
                FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
            )
        """)
        
        # Create Track table
        conn.execute("""
            CREATE TABLE Track (
                TrackId INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                AlbumId INTEGER NOT NULL,
                FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId)
            )
        """)
        
        # Create Customer table
        conn.execute("""
            CREATE TABLE Customer (
                CustomerId INTEGER PRIMARY KEY,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL
            )
        """)
        
        # Create Invoice table
        conn.execute("""
            CREATE TABLE Invoice (
                InvoiceId INTEGER PRIMARY KEY,
                CustomerId INTEGER NOT NULL,
                Total REAL NOT NULL,
                FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
            )
        """)
        
        # Insert test data
        # Artists
        artists = [
            (1, "AC/DC"),
            (2, "Led Zeppelin"),
            (3, "Pink Floyd"),
        ]
        conn.executemany("INSERT INTO Artist (ArtistId, Name) VALUES (?, ?)", artists)
        
        # Albums
        albums = [
            (1, "For Those About To Rock We Salute You", 1),
            (2, "Presence", 2),
            (3, "The Wall", 3),
        ]
        conn.executemany("INSERT INTO Album (AlbumId, Title, ArtistId) VALUES (?, ?, ?)", albums)
        
        # Tracks
        tracks = [
            (1, "For Those About To Rock (We Salute You)", 1),
            (2, "Rock and Roll", 2),
            (3, "In the Flesh?", 3),
        ]
        conn.executemany("INSERT INTO Track (TrackId, Name, AlbumId) VALUES (?, ?, ?)", tracks)
        
        # Customers
        customers = [
            (1, "John", "Doe"),
            (2, "Jane", "Smith"),
            (3, "Bob", "Johnson"),
            (4, "Alice", "Williams"),
            (5, "Charlie", "Brown"),
            (6, "Diana", "Davis"),
            (7, "Eve", "Miller"),
            (8, "Frank", "Wilson"),
            (9, "Grace", "Moore"),
            (10, "Henry", "Taylor"),
            (11, "Iris", "Anderson"),
            (12, "Jack", "Thomas"),
        ]
        conn.executemany(
            "INSERT INTO Customer (CustomerId, FirstName, LastName) VALUES (?, ?, ?)",
            customers
        )
        
        # Invoices - create data matching expected test results
        # test_top_invoices expects top[0][2] == 25.86 and top[2][2] == 21.86
        # Need 10 invoices with descending totals
        invoices = [
            (1, 1, 25.86),
            (2, 2, 24.50),
            (3, 3, 21.86),
            (4, 4, 20.75),
            (5, 5, 19.99),
            (6, 6, 18.50),
            (7, 7, 17.25),
            (8, 8, 16.00),
            (9, 9, 15.50),
            (10, 10, 14.99),
        ]
        conn.executemany(
            "INSERT INTO Invoice (InvoiceId, CustomerId, Total) VALUES (?, ?, ?)",
            invoices
        )
        
        conn.commit()
        yield conn
        
    finally:
        conn.close()
        # Clean up temporary file
        Path(temp_db_path).unlink(missing_ok=True)


@pytest.fixture
def isolated_sql_query(temp_db: sqlite3.Connection, monkeypatch) -> None:
    """Fixture to redirect SQL module to temporary database and isolate connections.
    
    This fixture:
    1. Patches the DB_PATH in the SQL module to point to the temporary database
    2. Resets the module-level connection cache before the test
    3. Closes and resets the connection cache after the test
    
    Args:
        temp_db: The temporary database fixture
        monkeypatch: Pytest's monkeypatch fixture
    """
    # Get the path from the connection's database attribute
    temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
    
    # Patch DB_PATH to point to temporary database
    monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
    
    # Reset module-level connection cache before test
    sql_query_module._conn = None
    
    yield
    
    # Close and reset connection cache after test
    if sql_query_module._conn is not None:
        sql_query_module._conn.close()
    sql_query_module._conn = None
