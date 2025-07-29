"""
Flyway-style database migrations implementation.
"""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from src.evolvishub_sqlite_adapter.utils.exceptions import MigrationError


class FlywayMigration:
    """
    Flyway-style database migrations manager.
    
    This class implements a simple version of Flyway's migration system for SQLite,
    supporting versioned migrations with a V{version}__{description}.sql naming pattern.
    
    Attributes:
        migrations_dir (Path): Directory containing migration files
        version_table (str): Name of the table to track migrations
    """
    
    def __init__(self, migrations_dir: str, version_table: str = "schema_version"):
        """
        Initialize the migrations manager.
        
        Args:
            migrations_dir (str): Path to migrations directory
            version_table (str): Name of the version tracking table
        """
        self.migrations_dir = Path(migrations_dir)
        self.version_table = version_table
        
        if not self.migrations_dir.exists():
            raise MigrationError(f"Migrations directory not found: {migrations_dir}")
    
    def _get_migration_files(self) -> List[Path]:
        """
        Get all migration files in version order.
        
        Returns:
            List[Path]: List of migration file paths
        """
        files = []
        for file in self.migrations_dir.glob("V*.sql"):
            try:
                version = int(file.stem.split("__")[0][1:])
                files.append((version, file))
            except (ValueError, IndexError):
                continue
        
        return [f[1] for f in sorted(files)]
    
    def _create_version_table(self, conn) -> None:
        """
        Create the version tracking table if it doesn't exist.
        
        Args:
            conn: Database connection
        """
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.version_table} (
                version INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                script TEXT NOT NULL,
                installed_on TIMESTAMP NOT NULL,
                execution_time INTEGER NOT NULL,
                success BOOLEAN NOT NULL
            )
        """)
    
    def _get_installed_versions(self, conn) -> List[int]:
        """
        Get list of installed migration versions.
        
        Args:
            conn: Database connection
            
        Returns:
            List[int]: List of installed version numbers
        """
        cursor = conn.execute(f"SELECT version FROM {self.version_table} WHERE success = 1")
        return [row[0] for row in cursor.fetchall()]
    
    def migrate(self, conn) -> None:
        """
        Run all pending migrations.
        
        Args:
            conn: Database connection
        """
        self._create_version_table(conn)
        installed_versions = self._get_installed_versions(conn)
        
        for migration_file in self._get_migration_files():
            version = int(migration_file.stem.split("__")[0][1:])
            
            if version in installed_versions:
                continue
            
            description = migration_file.stem.split("__")[1]
            script = migration_file.read_text()
            
            start_time = time.time()
            try:
                conn.executescript(script)
                conn.execute(
                    f"""
                    INSERT INTO {self.version_table}
                    (version, description, script, installed_on, execution_time, success)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        version,
                        description,
                        script,
                        datetime.now(),
                        int((time.time() - start_time) * 1000),
                        True,
                    ),
                )
            except Exception as e:
                conn.execute(
                    f"""
                    INSERT INTO {self.version_table}
                    (version, description, script, installed_on, execution_time, success)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        version,
                        description,
                        script,
                        datetime.now(),
                        int((time.time() - start_time) * 1000),
                        False,
                    ),
                )
                raise MigrationError(f"Migration failed: {str(e)}")
    
    def info(self, conn) -> List[Dict[str, Any]]:
        """
        Get information about all migrations.
        
        Args:
            conn: Database connection
            
        Returns:
            List[Dict[str, Any]]: List of migration information
        """
        cursor = conn.execute(f"SELECT * FROM {self.version_table} ORDER BY version")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()] 