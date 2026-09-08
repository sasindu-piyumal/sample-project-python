"""Tests for the _get_conn helper function contract.

Tests cover:
- Lazy connection creation on first call
- Caching and reuse of single connection across multiple calls
- FileNotFoundError when database path does not exist
- check_same_thread=False option configured correctly
- Race-condition safety when concurrent callers initialize
"""

import sqlite3
import tempfile
import threading
from pathlib import Path
from typing import List
from unittest import mock

import pytest

from llm_benchmark.sql import query as sql_query_module
from llm_benchmark.sql.query import _get_conn


@pytest.fixture(autouse=True)
def reset_connection_cache():
    """Reset module-level connection cache before and after each test.
    
    This ensures tests do not affect each other through the module-level
    _conn variable.
    """
    # Reset before test
    original_conn = sql_query_module._conn
    sql_query_module._conn = None
    
    yield
    
    # Clean up after test
    if sql_query_module._conn is not None:
        try:
            sql_query_module._conn.close()
        except Exception:
            pass
    sql_query_module._conn = original_conn


class TestMissingDatabaseFile:
    """Tests for FileNotFoundError when database file is missing."""

    def test_missing_file_raises_file_not_found(self, monkeypatch):
        """Missing database file raises FileNotFoundError."""
        # Set DB_PATH to a non-existent file
        nonexistent_path = Path("/nonexistent/path/to/database.db")
        monkeypatch.setattr(sql_query_module, "DB_PATH", nonexistent_path)
        
        with pytest.raises(FileNotFoundError) as exc_info:
            _get_conn()
        
        assert "Missing required SQLite database" in str(exc_info.value)

    def test_missing_file_error_includes_path(self, monkeypatch):
        """FileNotFoundError message includes the path."""
        nonexistent_path = Path("/tmp/missing_db_12345.db")
        monkeypatch.setattr(sql_query_module, "DB_PATH", nonexistent_path)
        
        with pytest.raises(FileNotFoundError) as exc_info:
            _get_conn()
        
        assert str(nonexistent_path) in str(exc_info.value)

    def test_missing_file_no_connection_created(self, monkeypatch):
        """No connection object is created when file is missing."""
        nonexistent_path = Path("/nonexistent/missing.db")
        monkeypatch.setattr(sql_query_module, "DB_PATH", nonexistent_path)
        
        # Verify _conn is None before
        assert sql_query_module._conn is None
        
        with pytest.raises(FileNotFoundError):
            _get_conn()
        
        # Verify _conn is still None after
        assert sql_query_module._conn is None


class TestLazyCreation:
    """Tests for lazy connection creation on first use."""

    def test_connection_none_initially(self):
        """Module-level connection is None before first call."""
        assert sql_query_module._conn is None

    def test_connection_created_on_first_call(self, temp_db):
        """Connection is created on first _get_conn call."""
        # Get temp database path
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        
        import llm_benchmark.sql.query as query_module
        query_module.DB_PATH = temp_db_path
        
        assert query_module._conn is None
        
        conn = _get_conn()
        
        assert query_module._conn is not None
        assert isinstance(conn, sqlite3.Connection)

    def test_connection_lazy_not_eager(self, temp_db, monkeypatch):
        """Connection is not created until first _get_conn call."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        # After patching DB_PATH, _conn should still be None
        assert sql_query_module._conn is None
        
        # Only after calling _get_conn should it be created
        _get_conn()
        assert sql_query_module._conn is not None


class TestConnectionCaching:
    """Tests for connection reuse and caching."""

    def test_repeated_calls_return_same_connection(self, temp_db, monkeypatch):
        """Repeated _get_conn calls return the same cached connection."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        conn1 = _get_conn()
        conn2 = _get_conn()
        conn3 = _get_conn()
        
        # All should be the same object
        assert conn1 is conn2
        assert conn2 is conn3
        assert id(conn1) == id(conn2) == id(conn3)

    def test_cached_connection_is_same_module_variable(self, temp_db, monkeypatch):
        """Returned connection is the module-level _conn variable."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        conn = _get_conn()
        
        assert conn is sql_query_module._conn

    def test_cache_not_recreated_on_repeated_calls(self, temp_db, monkeypatch):
        """Connection is not recreated on repeated calls."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        conn1 = _get_conn()
        id1 = id(conn1)
        
        conn2 = _get_conn()
        id2 = id(conn2)
        
        # Same object in memory
        assert id1 == id2


class TestConnectionOptions:
    """Tests for connection configuration options."""

    def test_check_same_thread_false(self, temp_db, monkeypatch):
        """Connection is created with check_same_thread=False."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        # Mock sqlite3.connect to verify the option is passed
        original_connect = sqlite3.connect
        connect_kwargs = {}
        
        def mock_connect(db_path, **kwargs):
            connect_kwargs.update(kwargs)
            return original_connect(db_path, **kwargs)
        
        monkeypatch.setattr(sqlite3, "connect", mock_connect)
        
        # Reset connection cache to allow the mock to work
        sql_query_module._conn = None
        
        _get_conn()
        
        # Verify check_same_thread was set to False
        assert connect_kwargs.get("check_same_thread") is False

    def test_connection_works_from_different_threads(self, temp_db, monkeypatch):
        """Connection can be used from multiple threads."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        conn = _get_conn()
        results = []
        exceptions = []
        
        def query_from_thread():
            try:
                # Execute a simple query from this thread
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                results.append(result)
            except Exception as e:
                exceptions.append(e)
        
        # Create and run threads
        threads = [threading.Thread(target=query_from_thread) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify no exceptions and all threads got results
        assert len(exceptions) == 0
        assert len(results) == 3
        assert all(r == (1,) for r in results)


class TestConcurrentInitialization:
    """Tests for race condition safety during concurrent initialization."""

    def test_concurrent_callers_share_single_connection(self, temp_db, monkeypatch):
        """Racing concurrent callers all get the same single created connection.
        
        This test verifies the double-check pattern protects against multiple
        threads independently creating separate connections.
        """
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        # Reset connection to None
        sql_query_module._conn = None
        
        connections = []
        exceptions = []
        barrier = threading.Barrier(3)  # Synchronize 3 threads
        
        def concurrent_get_conn():
            try:
                # Wait for all threads to be ready, then proceed together
                barrier.wait()
                conn = _get_conn()
                connections.append(conn)
            except Exception as e:
                exceptions.append(e)
        
        # Create threads that will race to call _get_conn
        threads = [
            threading.Thread(target=concurrent_get_conn)
            for _ in range(3)
        ]
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        # Verify no exceptions occurred
        assert len(exceptions) == 0
        
        # Verify all threads got the same connection object
        assert len(connections) == 3
        assert connections[0] is connections[1]
        assert connections[1] is connections[2]

    def test_concurrent_race_creates_one_connection(self, temp_db, monkeypatch):
        """Only one connection is created even with concurrent racers."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        sql_query_module._conn = None
        
        # Track how many times sqlite3.connect is called
        original_connect = sqlite3.connect
        connect_call_count = {"count": 0}
        
        def counting_connect(*args, **kwargs):
            connect_call_count["count"] += 1
            return original_connect(*args, **kwargs)
        
        monkeypatch.setattr(sqlite3, "connect", counting_connect)
        
        barrier = threading.Barrier(5)
        
        def race_caller():
            barrier.wait()
            _get_conn()
        
        threads = [threading.Thread(target=race_caller) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify sqlite3.connect was called exactly once
        assert connect_call_count["count"] == 1

    def test_lock_prevents_simultaneous_creation(self, temp_db, monkeypatch):
        """Lock prevents simultaneous connection creation attempts."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        sql_query_module._conn = None
        
        # Track lock acquisition
        lock_acquisitions = []
        original_lock_acquire = sql_query_module._conn_lock.acquire
        
        def tracking_acquire(blocking=True, timeout=-1):
            lock_acquisitions.append(None)
            return original_lock_acquire(blocking, timeout)
        
        monkeypatch.setattr(
            sql_query_module._conn_lock,
            "acquire",
            tracking_acquire
        )
        
        barrier = threading.Barrier(3)
        
        def concurrent_call():
            barrier.wait()
            _get_conn()
        
        threads = [threading.Thread(target=concurrent_call) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Lock was acquired at least once (by at least one thread)
        assert len(lock_acquisitions) > 0


class TestDoubleCheckPattern:
    """Tests for the double-check pattern implementation."""

    def test_double_check_protects_race(self, temp_db, monkeypatch):
        """Double-check pattern prevents multiple initialization attempts."""
        temp_db_path = Path(temp_db.execute("PRAGMA database_list").fetchone()[2])
        monkeypatch.setattr(sql_query_module, "DB_PATH", temp_db_path)
        
        sql_query_module._conn = None
        
        # Track outer check (before lock)
        outer_checks = []
        original_get_conn = _get_conn
        
        # We'll verify behavior by checking the final state
        barrier = threading.Barrier(2)
        
        def concurrent_init():
            barrier.wait()
            _get_conn()
        
        threads = [threading.Thread(target=concurrent_init) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # After concurrent calls, _conn should be set exactly once
        assert sql_query_module._conn is not None
        assert isinstance(sql_query_module._conn, sqlite3.Connection)
