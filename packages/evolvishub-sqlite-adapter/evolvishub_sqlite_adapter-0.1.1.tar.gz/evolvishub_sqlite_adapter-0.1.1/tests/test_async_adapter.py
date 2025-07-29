"""
Tests for the async SQLite adapter.
"""

import pytest
from src.evolvishub_sqlite_adapter.utils.exceptions import QueryError, TransactionError


@pytest.mark.asyncio
async def test_connection_pool(async_adapter):
    """Test connection pool initialization."""
    assert async_adapter._pool is not None
    assert async_adapter._pool.qsize() == 2


@pytest.mark.asyncio
async def test_execute(async_adapter):
    """Test execute method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    await async_adapter.execute(
        "INSERT INTO test (name) VALUES (?)",
        ("test",)
    )
    
    result = await async_adapter.fetch_one(
        "SELECT name FROM test WHERE id = ?",
        (1,)
    )
    assert result["name"] == "test"


@pytest.mark.asyncio
async def test_fetch_all(async_adapter):
    """Test fetch_all method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    await async_adapter.execute(
        "INSERT INTO test (name) VALUES (?), (?)",
        ("test1", "test2")
    )
    
    results = await async_adapter.fetch_all("SELECT * FROM test ORDER BY id")
    assert len(results) == 2
    assert results[0]["name"] == "test1"
    assert results[1]["name"] == "test2"


@pytest.mark.asyncio
async def test_transaction(async_adapter):
    """Test transaction context manager."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    
    async with async_adapter.transaction():
        await async_adapter.execute(
            "INSERT INTO test (name) VALUES (?)",
            ("test",)
        )
    
    result = await async_adapter.fetch_one("SELECT name FROM test")
    assert result["name"] == "test"


@pytest.mark.asyncio
async def test_transaction_rollback(async_adapter):
    """Test transaction rollback."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )

    with pytest.raises(TransactionError) as exc_info:
        async with async_adapter.transaction():
            await async_adapter.execute(
                "INSERT INTO test (name) VALUES (?)",
                ("test",)
            )
            raise Exception("Rollback test")
    assert 'Rollback test' in str(exc_info.value)

    result = await async_adapter.fetch_one("SELECT COUNT(*) as count FROM test")
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_invalid_query(async_adapter):
    """Test handling of invalid queries."""
    with pytest.raises(QueryError) as exc_info:
        await async_adapter.execute("INVALID SQL")
    assert 'near "INVALID": syntax error' in str(exc_info.value)


@pytest.mark.asyncio
async def test_connection_cleanup(async_adapter):
    """Test connection cleanup."""
    await async_adapter.close()
    assert async_adapter._pool is None 