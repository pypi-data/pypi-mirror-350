import os
import sqlite3
import tempfile
import unittest

import pandas as pd

from src.evolvishub_sqlite_adapter import SyncSQLiteAdapter, DatabaseConfig
from src.evolvishub_sqlite_adapter.dataframe_adapter import SQLiteDataFrameAdapter
from src.evolvishub_sqlite_adapter.utils.exceptions import QueryError, TransactionError


class TestSyncSQLiteAdapter(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.config = DatabaseConfig(database=self.temp_db.name)
        self.db = SyncSQLiteAdapter(self.config)
        self.db.connect()

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_init_invalid_path(self):
        """Test initialization with invalid database path."""
        from evolvishub_sqlite_adapter import DatabaseConfig
        with self.assertRaises(ValueError):
            SyncSQLiteAdapter(DatabaseConfig(database=""))
        with self.assertRaises(ValueError):
            SyncSQLiteAdapter(DatabaseConfig(database=None))

    def test_create_table(self):
        """Test creating a table with a direct query."""
        query = """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
        self.db.create_table(query)

        # Verify the table was created
        schema = self.db.get_table_schema("test_table")
        self.assertEqual(len(schema), 2)
        self.assertEqual(schema[0]["name"], "id")
        self.assertEqual(schema[1]["name"], "name")

    def test_create_table_invalid_query(self):
        """Test creating a table with invalid query."""
        with self.assertRaises(ValueError):
            self.db.create_table("")
        with self.assertRaises(QueryError) as cm:
            self.db.create_table("INVALID SQL")
        self.assertIn('near "INVALID": syntax error', str(cm.exception))

    def test_create_table_from_file(self):
        """Test creating a table from a SQL file."""
        # Create a temporary SQL file
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".sql"
        ) as temp_sql:
            temp_sql.write(
                """
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
            )
            temp_sql_path = temp_sql.name

        try:
            # Test creating a table from file
            self.db.create_table_from_file(temp_sql_path)

            # Verify the table was created
            schema = self.db.get_table_schema("test_table")
            self.assertEqual(len(schema), 2)
            self.assertEqual(schema[0]["name"], "id")
            self.assertEqual(schema[1]["name"], "name")
        finally:
            # Clean up the temporary SQL file
            os.unlink(temp_sql_path)

    def test_create_table_from_nonexistent_file(self):
        """Test creating a table from a nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            self.db.create_table_from_file("nonexistent.sql")

    def test_execute_query_positional_params(self):
        """Test executing a query with positional parameters."""
        # Create a table
        self.db.create_table(
            """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
        )

        # Insert data
        self.db.execute_query(
            "INSERT INTO test_table (name) VALUES (?)", ("test_name",)
        )

        # Query data
        results = self.db.fetch_all("SELECT * FROM test_table")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "test_name")

    def test_execute_query_named_params(self):
        """Test executing a query with named parameters."""
        # Create a table
        self.db.create_table(
            """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
        )

        # Insert data
        self.db.execute_query(
            "INSERT INTO test_table (name) VALUES (:name)", {"name": "test_name"}
        )

        # Query data
        results = self.db.fetch_all("SELECT * FROM test_table")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "test_name")

    def test_execute_query_invalid_query(self):
        """Test executing an invalid query."""
        with self.assertRaises(ValueError):
            self.db.execute_query("")
        with self.assertRaises(QueryError) as cm:
            self.db.execute_query("INVALID SQL")
        self.assertIn('near "INVALID": syntax error', str(cm.exception))

    def test_transaction_commit(self):
        """Test successful transaction commit."""
        self.db.create_table(
            """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
        )

        with self.db.transaction():
            self.db.execute_query(
                "INSERT INTO test_table (name) VALUES (?)", ("test_name",)
            )

        results = self.db.fetch_all("SELECT * FROM test_table")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "test_name")

    def test_transaction_rollback(self):
        """Test transaction rollback on error."""
        self.db.create_table(
            """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
        )

        with self.assertRaises(TransactionError) as cm:
            with self.db.transaction():
                self.db.execute_query(
                    "INSERT INTO test_table (name) VALUES (?)", ("test_name",)
                )
                # This will cause an error and rollback
                self.db.execute_query("INVALID SQL")
        self.assertIn('near "INVALID": syntax error', str(cm.exception))

        results = self.db.fetch_all("SELECT * FROM test_table")
        self.assertEqual(len(results), 0)

    def test_table_exists(self):
        """Test checking if a table exists."""
        self.assertFalse(self.db.table_exists("test_table"))

        self.db.create_table(
            """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY
        )
        """
        )

        self.assertTrue(self.db.table_exists("test_table"))
        self.assertFalse(self.db.table_exists("nonexistent_table"))

    def test_table_exists_invalid_name(self):
        """Test checking table existence with invalid name."""
        with self.assertRaises(ValueError):
            self.db.table_exists("")
        with self.assertRaises(ValueError):
            self.db.table_exists(None)

    def test_context_manager(self):
        """Test using the adapter as a context manager."""
        from evolvishub_sqlite_adapter import DatabaseConfig
        with SyncSQLiteAdapter(DatabaseConfig(database=self.temp_db.name)) as db:
            db.create_table(
                """
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
            )
            db.execute_query("INSERT INTO test_table (name) VALUES (?)", ("test_name",))

        # Adapter should be reusable after context manager
        self.db.create_table(
            """
        CREATE TABLE IF NOT EXISTS another_table (
            id INTEGER PRIMARY KEY
        )
        """
        )
        self.db.execute_query("INSERT INTO another_table (id) VALUES (?)", (1,))
        results = self.db.fetch_all("SELECT * FROM another_table")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], 1)


class TestSQLiteDataFrameAdapter(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = SQLiteDataFrameAdapter(self.temp_db.name)

    def tearDown(self):
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_fetch_dataframe(self):
        # Create a table and insert data
        self.db.create_table(
            """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
        )
        self.db.execute_query("INSERT INTO test_table (name) VALUES (?)", ("Alice",))
        self.db.execute_query("INSERT INTO test_table (name) VALUES (?)", ("Bob",))
        # Fetch as DataFrame
        df = self.db.fetch_dataframe("SELECT * FROM test_table")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (2, 2))
        self.assertIn("name", df.columns)
        self.assertListEqual(sorted(df["name"].tolist()), ["Alice", "Bob"])


if __name__ == "__main__":
    unittest.main()
