# Legion Query Runners

This package provides query runners for Legion, supporting various database systems and data sources. The package provides a unified interface for executing queries, retrieving schemas, and handling result sets across different database systems.

## Supported Data Sources

- PostgreSQL
- Redshift
- CockroachDB
- MySQL
- RDS MySQL
- Microsoft SQL Server
- Big Query
- Oracle DB
- SQLite

## Installation

```bash
pip install legion-query-runner
```

## Basic Usage

```python
from legion_query_runner.query_runner import QueryRunner

# Initialize with database configuration
sqlite_config = {
    "database": "/path/to/your/database.sqlite"
}

# Example with SSH tunnel configuration
pg_config = {
    "host": "internal-db.example.com",
    "port": 5432,
    "user": "username",
    "password": "password",
    "dbname": "database_name",
    "ssh_tunnel_enabled": True,
    "ssh_host": "bastion.example.com",
    "ssh_port": 22,
    "ssh_username": "ssh_user"
}

# Create a QueryRunner instance
runner = QueryRunner('sqlite', sqlite_config)

# Test connection
runner.test_connection()

# Execute a query
results = runner.run_query("SELECT * FROM users LIMIT 10")
print(f"Columns: {results['columns']}")
print(f"Row count: {len(results['rows'])}")

# Get schema
schema = runner.get_schema()
for table in schema:
    print(f"Table: {table['name']}")
    for column in table['columns']:
        print(f"  - {column['name']} ({column['type']})")

# Get columns for a specific table
columns = runner.get_table_columns("users")
print(f"Columns in users table: {columns}")

# Get column types for a specific table
column_types = runner.get_table_types("users")
print(f"Column types in users table: {column_types}")
```

## Core Features

- **Unified Database Interface**: Interact with different databases using a consistent API
- **Schema Retrieval**: Get table and column information from your database
- **Type Inference**: Automatic detection of column data types
- **Query Execution**: Run SQL queries and process results in a standardized format
- **Connection Management**: Establish, test, and maintain database connections
- **SSH Tunneling**: Connect to databases through SSH tunnels with bastion host support
- **Authentication Support**: Handle various authentication methods including IAM for AWS services

## Development

To set up the development environment:

1. Install dependencies:
   ```bash
   poetry install --with dev
   ```

2. Run tests:
   ```bash
   poetry run pytest
   ```

## Publish

```
poetry publish --build
```

## License

Proprietary - All rights reserved by Legion. 