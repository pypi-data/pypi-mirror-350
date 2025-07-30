"""
Legion Query Runners
~~~~~~~~~~~~~~~~~~

A package providing unified database query runners for various database systems.
"""

from typing import Dict, List, Optional, Union, Any

__version__ = "0.1.0"
__author__ = "Legion"
__email__ = "info@thelegionai.com"

from .query_runner.base import (
    TYPE_STRING,
    TYPE_INTEGER,
    TYPE_FLOAT,
    TYPE_BOOLEAN,
    TYPE_DATETIME,
    TYPE_DATE,
    BaseQueryRunner,
    BaseSQLQueryRunner,
    InterruptException,
    JobTimeoutException,
    QueryRunner,
)

# Database types
DB_MYSQL = "mysql"
DB_POSTGRESQL = "postgresql"
DB_MSSQL = "mssql"
DB_REDSHIFT = "redshift"

__all__ = [
    "QueryRunner",
    "TYPE_STRING",
    "TYPE_INTEGER",
    "TYPE_FLOAT",
    "TYPE_BOOLEAN",
    "TYPE_DATETIME",
    "TYPE_DATE",
    "DB_MYSQL",
    "DB_POSTGRESQL",
    "DB_MSSQL",
    "DB_REDSHIFT",
    "BaseQueryRunner",
    "BaseSQLQueryRunner",
    "InterruptException",
    "JobTimeoutException",
] 