"""
Tests for the Flyway-style migration system.
"""

import os
import tempfile
from pathlib import Path
import pytest
import sqlite3

from evolvishub_sqlite_adapter import SyncSQLiteAdapter, DatabaseConfig
from evolvishub_sqlite_adapter.migrations import FlywayMigration
from evolvishub_sqlite_adapter.utils.exceptions import MigrationError


@pytest.fixture
def migrations_dir():
    """Create a temporary directory for migration files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def migration_files(migrations_dir):
    """Create test migration files."""
    # Create V1 migration
    v1_file = migrations_dir / "V1__create_users_table.sql"
    v1_file.write_text("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create V2 migration
    v2_file = migrations_dir / "V2__add_email_column.sql"
    v2_file.write_text("""
        ALTER TABLE users ADD COLUMN email TEXT;
    """)
    
    # Create V3 migration
    v3_file = migrations_dir / "V3__create_posts_table.sql"
    v3_file.write_text("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    
    return [v1_file, v2_file, v3_file]


def test_migration_initialization(migrations_dir):
    """Test migration manager initialization."""
    migrations = FlywayMigration(migrations_dir)
    assert migrations.migrations_dir == Path(migrations_dir)
    assert migrations.version_table == "schema_version"


def test_migration_execution(db_config, migration_files):
    """Test migration execution."""
    db = SyncSQLiteAdapter(db_config)
    db.connect()
    
    migrations = FlywayMigration(migration_files[0].parent)
    
    # Run migrations
    with db.transaction() as conn:
        migrations.migrate(conn)
    
    # Verify tables were created
    assert db.table_exists("users")
    assert db.table_exists("posts")
    
    # Verify schema
    users_schema = db.get_table_schema("users")
    assert len(users_schema) == 4  # id, name, created_at, email
    assert any(col["name"] == "email" for col in users_schema)
    
    posts_schema = db.get_table_schema("posts")
    assert len(posts_schema) == 5  # id, user_id, title, content, created_at
    
    db.close()


def test_migration_info(db_config, migration_files):
    """Test migration info retrieval."""
    db = SyncSQLiteAdapter(db_config)
    db.connect()
    
    migrations = FlywayMigration(migration_files[0].parent)
    
    # Run migrations
    with db.transaction() as conn:
        migrations.migrate(conn)
    
    # Get migration info
    with db.transaction() as conn:
        info = migrations.info(conn)
    
    assert len(info) == 3
    assert info[0]["version"] == 1
    assert info[0]["description"] == "create_users_table"
    assert info[1]["version"] == 2
    assert info[1]["description"] == "add_email_column"
    assert info[2]["version"] == 3
    assert info[2]["description"] == "create_posts_table"
    
    db.close()


def test_migration_version_ordering(db_config, migration_files):
    """Test migration version ordering."""
    db = SyncSQLiteAdapter(db_config)
    db.connect()
    
    # Create migrations in sequential order with unique versions
    v4_file = migration_files[0].parent / "V4__fourth_migration.sql"
    v4_file.write_text("CREATE TABLE fourth (id INTEGER PRIMARY KEY);")
    
    v5_file = migration_files[0].parent / "V5__fifth_migration.sql"
    v5_file.write_text("CREATE TABLE fifth (id INTEGER PRIMARY KEY);")
    
    migrations = FlywayMigration(migration_files[0].parent)
    
    # Run migrations
    with db.transaction() as conn:
        migrations.migrate(conn)
    
    # Get migration info
    with db.transaction() as conn:
        info = migrations.info(conn)
    
    # Verify migrations ran in correct order
    versions = [m["version"] for m in info]
    assert versions == sorted(versions)
    
    db.close() 