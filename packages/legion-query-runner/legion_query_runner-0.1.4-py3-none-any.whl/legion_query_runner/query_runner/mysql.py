import logging
import os
import threading
import json
from functools import wraps
from typing import Any, Dict, Optional, Tuple, cast, List

from .base import (
    TYPE_DATE,
    TYPE_DATETIME,
    TYPE_FLOAT,
    TYPE_INTEGER,
    TYPE_STRING,
    BaseSQLQueryRunner,
    InterruptException,
    JobTimeoutException,
    with_ssh_tunnel,
    register,
)
from ..settings.helpers import parse_boolean
from .utils import json_dumps

try:
    import MySQLdb

    enabled = True
except ImportError:
    enabled = False

logger = logging.getLogger(__name__)
types_map = {
    0: TYPE_FLOAT,
    1: TYPE_INTEGER,
    2: TYPE_INTEGER,
    3: TYPE_INTEGER,
    4: TYPE_FLOAT,
    5: TYPE_FLOAT,
    7: TYPE_DATETIME,
    8: TYPE_INTEGER,
    9: TYPE_INTEGER,
    10: TYPE_DATE,
    12: TYPE_DATETIME,
    15: TYPE_STRING,
    16: TYPE_INTEGER,
    246: TYPE_FLOAT,
    253: TYPE_STRING,
    254: TYPE_STRING,
}


class Result:
    def __init__(self):
        self.data = None
        self.error = None


class Mysql(BaseSQLQueryRunner):
    noop_query = "SELECT 1"

    def __init__(self, configuration: Dict[str, Any]):
        super().__init__(configuration)
        self._original_run_query = self.run_query
        self._ssh_details = None
        if configuration.get("ssh_tunnel_enabled"):
            self._ssh_details = {
                "ssh_host": configuration.get("ssh_host"),
                "ssh_port": configuration.get("ssh_port", 22),
                "ssh_username": configuration.get("ssh_username"),
            }

    @property
    def host(self):
        """Returns this query runner's configured host.
        This is used primarily for temporarily swapping endpoints when using SSH tunnels to connect to a data source.
        """
        if "host" in self.configuration:
            return self.configuration["host"]
        else:
            raise NotImplementedError()

    @host.setter
    def host(self, host):
        """Sets this query runner's configured host.
        This is used primarily for temporarily swapping endpoints when using SSH tunnels to connect to a data source.
        """
        if "host" in self.configuration:
            self.configuration["host"] = host
        else:
            raise NotImplementedError()

    @classmethod
    def configuration_schema(cls):
        show_ssl_settings = parse_boolean(os.environ.get("MYSQL_SHOW_SSL_SETTINGS", "true"))

        schema = {
            "type": "object",
            "properties": {
                "host": {"type": "string", "default": "127.0.0.1"},
                "user": {"type": "string"},
                "passwd": {"type": "string", "title": "Password"},
                "db": {"type": "string", "title": "Database name"},
                "port": {"type": "number", "default": 3306},
                "connect_timeout": {"type": "number", "default": 60, "title": "Connection Timeout"},
                "charset": {"type": "string", "default": "utf8"},
                "use_unicode": {"type": "boolean", "default": True},
                "autocommit": {"type": "boolean", "default": False},
                "ssh_tunnel_enabled": {"type": "boolean", "title": "Use SSH Tunnel", "default": False},
                "ssh_host": {"type": "string", "title": "SSH Host"},
                "ssh_port": {"type": "number", "title": "SSH Port", "default": 22},
                "ssh_username": {"type": "string", "title": "SSH Username"},
            },
            "order": [
                "host",
                "port",
                "user",
                "passwd",
                "db",
                "connect_timeout",
                "charset",
                "use_unicode",
                "autocommit",
                "ssh_tunnel_enabled",
                "ssh_host",
                "ssh_port",
                "ssh_username",
            ],
            "required": ["db"],
            "secret": ["passwd"],
        }

        if show_ssl_settings:
            schema["properties"].update(
                {
                    "ssl_mode": {
                        "type": "string",
                        "title": "SSL Mode",
                        "default": "preferred",
                        "extendedEnum": [
                            {"value": "disabled", "name": "Disabled"},
                            {"value": "preferred", "name": "Preferred"},
                            {"value": "required", "name": "Required"},
                            {"value": "verify-ca", "name": "Verify CA"},
                            {"value": "verify-identity", "name": "Verify Identity"},
                        ],
                    },
                    "use_ssl": {"type": "boolean", "title": "Use SSL"},
                    "ssl_cacert": {
                        "type": "string",
                        "title": "Path to CA certificate file to verify peer against (SSL)",
                    },
                    "ssl_cert": {
                        "type": "string",
                        "title": "Path to client certificate file (SSL)",
                    },
                    "ssl_key": {
                        "type": "string",
                        "title": "Path to private key file (SSL)",
                    },
                }
            )

        return schema

    @classmethod
    def name(cls):
        return "MySQL"

    @classmethod
    def enabled(cls):
        return enabled

    def _connection(self):
        params = dict(
            host=self.configuration.get("host", ""),
            user=self.configuration.get("user", ""),
            passwd=self.configuration.get("passwd", ""),
            db=self.configuration["db"],
            port=self.configuration.get("port", 3306),
            charset=self.configuration.get("charset", "utf8"),
            use_unicode=self.configuration.get("use_unicode", True),
            connect_timeout=self.configuration.get("connect_timeout", 60),
            autocommit=self.configuration.get("autocommit", True),
        )

        ssl_options = self._get_ssl_parameters()

        if ssl_options:
            params["ssl"] = ssl_options

        connection = MySQLdb.connect(**params)

        return connection

    def _get_tables(self, schema: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        query = """
        SELECT col.table_schema as table_schema,
               col.table_name as table_name,
               col.column_name as column_name
        FROM `information_schema`.`columns` col
        WHERE LOWER(col.table_schema) NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys');
        """

        results, error = self.run_query(query, None)

        if error is not None:
            self._handle_run_query_error(error)

        if results is None:
            return []

        results_dict = cast(Dict[str, List[Dict[str, Any]]], json.loads(results))
        for row in results_dict["rows"]:
            if cast(str, row["table_schema"]) != self.configuration["db"]:
                table_name = "{}.{}".format(
                    cast(str, row["table_schema"]), 
                    cast(str, row["table_name"])
                )
            else:
                table_name = cast(str, row["table_name"])

            if table_name not in schema:
                schema[table_name] = {"name": table_name, "columns": []}

            schema[table_name]["columns"].append(cast(str, row["column_name"]))

        return list(schema.values())

    def run_query(self, query: str, user: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        if self._ssh_details:
            if not all(self._ssh_details.get(k) for k in ["ssh_host", "ssh_username"]):
                raise KeyError("Missing required SSH configuration. Need ssh_host and ssh_username.")
            try:
                tunnel = with_ssh_tunnel(self, self._ssh_details)
                tunnel.__enter__()
                try:
                    result = self._run_query_impl(query, user)
                    tunnel.__exit__(None, None, None)
                    return result
                except Exception as e:
                    tunnel.__exit__(type(e), e, None)
                    raise
            except Exception as e:
                raise Exception(f"SSH tunnel: {str(e)}")
        return self._run_query_impl(query, user)

    def _run_query_impl(self, query: str, user: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        connection = None
        cursor = None

        try:
            connection = self._connection()
            cursor = connection.cursor()
            cursor.execute(query)

            if cursor.description is not None:
                columns = self.fetch_columns([(i[0], types_map.get(i[1], None)) for i in cursor.description])
                rows = [dict(zip((c['name'] for c in columns), row)) for row in cursor]

                data = {'columns': columns, 'rows': rows}
                error = None
                json_data = json_dumps(data)
            else:
                error = None
                json_data = json_dumps({'columns': [], 'rows': []})
        except MySQLdb.Error as e:
            json_data = None
            error = str(e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return json_data, error

    def _get_ssl_parameters(self):
        if not self.configuration.get("use_ssl"):
            return None

        ssl_params = {}

        if self.configuration.get("use_ssl"):
            config_map = {"ssl_mode": "preferred", "ssl_cacert": "ca", "ssl_cert": "cert", "ssl_key": "key"}
            for key, cfg in config_map.items():
                val = self.configuration.get(key)
                if val:
                    ssl_params[cfg] = val

        return ssl_params

    def _cancel(self, thread_id):
        connection = None
        cursor = None
        error = None

        try:
            connection = self._connection()
            cursor = connection.cursor()
            query = "KILL %d" % (thread_id)
            logging.debug(query)
            cursor.execute(query)
        except MySQLdb.Error as e:
            if cursor:
                cursor.close()
            error = e.args[1]
        finally:
            if connection:
                connection.close()

        return error


class RDSMySQL(Mysql):
    @classmethod
    def name(cls):
        return "MySQL (Amazon RDS)"

    @classmethod
    def type(cls):
        return "rds_mysql"

    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "host": {"type": "string"},
                "user": {"type": "string"},
                "passwd": {"type": "string", "title": "Password"},
                "db": {"type": "string", "title": "Database name"},
                "port": {"type": "number", "default": 3306},
                "use_ssl": {"type": "boolean", "title": "Use SSL"},
            },
            "order": ["host", "port", "user", "passwd", "db"],
            "required": ["db", "user", "passwd", "host"],
            "secret": ["passwd"],
        }

    def _get_ssl_parameters(self):
        if self.configuration.get("use_ssl"):
            ca_path = os.path.join(os.path.dirname(__file__), "./files/rds-combined-ca-bundle.pem")
            return {"ca": ca_path}

        return None


register(Mysql)
register(RDSMySQL)
