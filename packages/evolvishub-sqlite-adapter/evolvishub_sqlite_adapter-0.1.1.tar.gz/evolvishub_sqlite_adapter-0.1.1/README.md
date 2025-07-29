# Evolvishub SQLite Adapter

<div align="center">
  <img src="assets/png/eviesales.png" alt="Evolvishub SQLite Adapter Logo" width="200"/>
  <p><a href="https://evolvis.ai">Evolvis AI</a> - Empowering Innovation Through AI</p>
</div>

A robust SQLite adapter with both synchronous and asynchronous interfaces, featuring connection pooling, transaction support, and Flyway-style migrations.

## Features

- 🔄 Both synchronous and asynchronous interfaces
- 🔌 Connection pooling for better performance
- 🔒 Transaction support with context managers
- 📦 Flyway-style database migrations
- 📊 Pandas DataFrame integration
- 🛡️ Comprehensive error handling
- 📝 Detailed logging
- 🧪 Full test coverage

## Installation

```bash
pip install evolvishub-sqlite-adapter
```

## Quick Start

### Synchronous Usage

```python
from evolvishub_sqlite_adapter import SyncSQLiteAdapter, DatabaseConfig

# Configure the database
config = DatabaseConfig(
    database="my_database.db",
    pool_size=5,
    journal_mode="WAL",
    synchronous="NORMAL",
    foreign_keys=True
)

# Create adapter instance
db = SyncSQLiteAdapter(config)
db.connect()

# Execute queries
db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
db.execute("INSERT INTO users (name) VALUES (?)", ("John Doe",))

# Fetch results
results = db.fetch_all("SELECT * FROM users")

# Use transactions
with db.transaction():
    db.execute("INSERT INTO users (name) VALUES (?)", ("Jane Doe",))
    db.execute("UPDATE users SET name = ? WHERE id = ?", ("John Smith", 1))

# Close connections
db.close()
```

### Asynchronous Usage

```python
import asyncio
from evolvishub_sqlite_adapter import AsyncSQLiteAdapter, DatabaseConfig

async def main():
    # Configure the database
    config = DatabaseConfig(
        database="my_database.db",
        pool_size=5,
        journal_mode="WAL"
    )

    # Create adapter instance
    db = AsyncSQLiteAdapter(config)
    await db.connect()

    # Execute queries
    await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    await db.execute("INSERT INTO users (name) VALUES (?)", ("John Doe",))

    # Fetch results
    results = await db.fetch_all("SELECT * FROM users")

    # Use transactions
    async with db.transaction():
        await db.execute("INSERT INTO users (name) VALUES (?)", ("Jane Doe",))
        await db.execute("UPDATE users SET name = ? WHERE id = ?", ("John Smith", 1))

    # Close connections
    await db.close()

asyncio.run(main())
```

## Database Migrations

The package includes a Flyway-style migration system. Create your migration files in a directory with the naming pattern `V{version}__{description}.sql`.

### Migration File Structure

```
migrations/
├── V1__create_users_table.sql
├── V2__add_email_column.sql
└── V3__create_posts_table.sql
```

Example migration file (`V1__create_users_table.sql`):
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Using Migrations

```python
from evolvishub_sqlite_adapter import SyncSQLiteAdapter, DatabaseConfig
from evolvishub_sqlite_adapter.migrations import FlywayMigration

# Configure and connect to database
config = DatabaseConfig(database="my_database.db")
db = SyncSQLiteAdapter(config)
db.connect()

# Initialize migrations
migrations = FlywayMigration("migrations")

# Run migrations
with db.transaction():
    migrations.migrate(db._get_connection())

# Get migration info
migration_info = migrations.info(db._get_connection())
for info in migration_info:
    print(f"Version {info['version']}: {info['description']}")

db.close()
```

## Configuration

The `DatabaseConfig` class supports various SQLite configuration options:

```python
config = DatabaseConfig(
    database="my_database.db",      # Database file path
    pool_size=5,                    # Connection pool size
    journal_mode="WAL",            # Journal mode (WAL, DELETE, TRUNCATE, etc.)
    synchronous="NORMAL",          # Synchronous mode
    foreign_keys=True,             # Enable foreign key constraints
    check_same_thread=False,       # Allow connections from different threads
    cache_size=2000,              # SQLite cache size in pages
    temp_store="MEMORY",          # Temporary storage mode
    page_size=4096,               # Page size in bytes
    log_level="INFO",             # Logging level
    log_file="sqlite.log"         # Optional log file path
)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Evolvis AI - info@evolvis.ai

Project Link: [https://github.com/evolvis/evolvishub-sqlite-adapter](https://github.com/evolvis/evolvishub-sqlite-adapter)