import logging
import sqlite3

from .base import (
    BaseSQLQueryRunner,
    JobTimeoutException,
    register,
    TYPE_DATETIME,
    TYPE_FLOAT,
    TYPE_INTEGER,
    TYPE_STRING,
    TYPE_DATE,
    TYPE_BOOLEAN,
)

logger = logging.getLogger(__name__)


class Sqlite(BaseSQLQueryRunner):
    noop_query = "pragma quick_check"

    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {"dbpath": {"type": "string", "title": "Database Path"}},
            "required": ["dbpath"],
        }

    @classmethod
    def type(cls):
        return "sqlite"

    def __init__(self, configuration):
        super(Sqlite, self).__init__(configuration)

        self._dbpath = self.configuration.get("dbpath", "")

    def _map_sqlite_type(self, sqlite_type: str) -> str:
        """Map SQLite type to standardized type."""
        type_mapping = {
            'INTEGER': TYPE_INTEGER,
            'REAL': TYPE_FLOAT,
            'FLOAT': TYPE_FLOAT,
            'NUMERIC': TYPE_FLOAT,
            'TEXT': TYPE_STRING,
            'TIMESTAMP': TYPE_DATETIME,
            'DATETIME': TYPE_DATETIME,
            'DATE': TYPE_DATE,
            'BOOLEAN': TYPE_BOOLEAN,
        }
        sqlite_type = sqlite_type.upper().split('(')[0].strip()
        return type_mapping.get(sqlite_type, TYPE_STRING)

    def _get_tables(self, schema):
        query_table = "select tbl_name from sqlite_master where type='table'"
        query_columns = 'PRAGMA table_info("%s")'

        results, error = self.run_query(query_table, None)

        if error is not None:
            raise Exception("Failed getting schema.")

        if results is None:
            return []

        for row in results["rows"]:
            table_name = row["tbl_name"]
            schema[table_name] = {"name": table_name, "columns": []}
            results_table, error = self.run_query(query_columns % (table_name,), None)
            if error is not None:
                self._handle_run_query_error(error)

            if results_table is None:
                continue

            for row_column in results_table["rows"]:
                schema[table_name]["columns"].append({
                    "name": row_column["name"],
                    "type": self._map_sqlite_type(row_column["type"])
                })

        return list(schema.values())

    def run_query(self, query, user):
        connection = sqlite3.connect(self._dbpath)

        cursor = connection.cursor()

        try:
            cursor.execute(query)
            connection.commit()  # Commit changes for INSERT/UPDATE/DELETE queries

            if cursor.description is not None:
                columns = self.fetch_columns([(i[0], None) for i in cursor.description])
                rows = [dict(zip((column["name"] for column in columns), row)) for row in cursor]
                data = {"columns": columns, "rows": rows}
            else:
                # Query executed successfully but returned no data (e.g., INSERT/UPDATE)
                data = {"columns": [], "rows": [], "affected_rows": cursor.rowcount}
            error = None
        except (KeyboardInterrupt, JobTimeoutException):
            # SQLite doesn't support connection cancellation like other DB engines
            # Just close the connection and re-raise the exception
            connection.close()
            raise
        except Exception as e:
            error = str(e)
            data = None
        finally:
            connection.close()
        return data, error


register(Sqlite)
