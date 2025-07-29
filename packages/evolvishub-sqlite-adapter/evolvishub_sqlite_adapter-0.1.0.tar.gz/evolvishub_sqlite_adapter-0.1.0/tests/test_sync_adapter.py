"""
Tests for the sync SQLite adapter.
"""

import pytest

from src.evolvishub_sqlite_adapter.utils.exceptions import QueryError, TransactionError


def test_connection_pool(sync_adapter):
    """Test connection pool initialization."""
    assert sync_adapter._pool is not None
    assert sync_adapter._pool.qsize() == 2


def test_execute(sync_adapter):
    """Test execute method."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    sync_adapter.execute(
        "INSERT INTO test (name) VALUES (?)",
        ("test",)
    )
    
    result = sync_adapter.fetch_one(
        "SELECT name FROM test WHERE id = ?",
        (1,)
    )
    assert result["name"] == "test"


def test_fetch_all(sync_adapter):
    """Test fetch_all method."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    sync_adapter.execute(
        "INSERT INTO test (name) VALUES (?), (?)",
        ("test1", "test2")
    )
    
    results = sync_adapter.fetch_all("SELECT * FROM test ORDER BY id")
    assert len(results) == 2
    assert results[0]["name"] == "test1"
    assert results[1]["name"] == "test2"


def test_transaction(sync_adapter):
    """Test transaction context manager."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    
    with sync_adapter.transaction():
        sync_adapter.execute(
            "INSERT INTO test (name) VALUES (?)",
            ("test",)
        )
    
    result = sync_adapter.fetch_one("SELECT name FROM test")
    assert result["name"] == "test"


def test_transaction_rollback(sync_adapter):
    """Test transaction rollback."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )

    def do_transaction():
        with sync_adapter.transaction():
            sync_adapter.execute(
                "INSERT INTO test (name) VALUES (?)",
                ("test",)
            )
            raise Exception("Rollback test")

    with pytest.raises(TransactionError) as exc_info:
        do_transaction()
    assert 'Rollback test' in str(exc_info.value)


def test_invalid_query(sync_adapter):
    """Test handling of invalid queries."""
    with pytest.raises(QueryError) as exc_info:
        sync_adapter.execute("INVALID SQL")
    assert 'near "INVALID": syntax error' in str(exc_info.value)


def test_connection_cleanup(sync_adapter):
    """Test connection cleanup."""
    sync_adapter.close()
    assert sync_adapter._pool is None 