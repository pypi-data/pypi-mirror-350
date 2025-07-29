# Copyright (C) 2025, IQMO Corporation [support@iqmo.com]
# All Rights Reserved

import logging
import os
from dataclasses import dataclass

import pyodbc
from pandas import DataFrame, read_sql

from ... import IqlExtension, SubQuery, register_extension
from ...datamodel import cache

logger = logging.getLogger(__name__)
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.engine import URL

# https://github.com/pymssql/pymssql
# https://pymssql.readthedocs.io/en/stable/


# The connection cache is either connections **or** options to create a connection
_CONNECTION_CACHE: dict[str, sa.Engine | dict] = {}


def _get_connection_from_options(connection_string: str, **kwargs) -> sa.Engine:
        
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

    engine = create_engine(connection_url)

    return engine

def _get_connection(connection_name: str) -> pyodbc.Connection:
    existing_conn: sa.Engine | dict = _CONNECTION_CACHE[connection_name]
    if isinstance(existing_conn, dict):
        return _get_connection_from_options(**existing_conn)
    else:
        return existing_conn


def _execute_query(engine: sa.Engine, query: str, parameters: dict | None = None) -> DataFrame:
    logger.debug("Executing query in sqlalchemy: %s", query)
    
    with engine.begin() as conn:
        return read_sql(sql=query, con=conn, params=parameters)
    

@dataclass
class SqlServerExtensionPyOdbcConnect(IqlExtension):
    def executeimpl(self, sq: SubQuery) -> DataFrame:
        connection_name: str = sq.options.get("name", "default")  # type: ignore
        connection_string: str = sq.options["connection_string"]  # type: ignore

        eager = sq.options.get("eager", True)
        conn_options = {
            k: v for k, v in sq.options.items() if k != "name" and k != "eager" and k != "connection_string"
        }

        if eager:
            _CONNECTION_CACHE[connection_name] = _get_connection_from_options(
                connection_string=connection_string, **conn_options
            )
        else:
            _CONNECTION_CACHE[connection_name] = conn_options

        return DataFrame({"success": [True], "message": ["Connection Successful"]})


@dataclass
class SqlServerExtensionPyOdbc(IqlExtension):
    @cache.iql_cache
    def executeimpl(self, sq: SubQuery) -> DataFrame:
        connection_name: str = sq.options.get("name", "default")  # type: ignore

        conn: pyodbc.Connection = _get_connection(connection_name)

        query: str = sq.get_query()  # type: ignore

        parameters: dict = sq.options.get("PARAMETERS", None)  # type: ignore

        return _execute_query(conn, query, parameters=parameters)


def register(keyword: str):
    cache_maxage = os.environ.get("IQL_MSSQL_CACHE_MAXAGE", None)
    if cache_maxage is not None:
        cache_maxage = int(cache_maxage)


    extension = SqlServerExtensionPyOdbc(keyword=keyword)
    extension.cache = cache.MemoryCache(max_age=cache_maxage, min_cost=2)
    register_extension(extension)

    extension = SqlServerExtensionPyOdbcConnect(keyword=keyword, subword="pyodbc_connect")
    register_extension(extension)

    extension = SqlServerExtensionPyOdbc(keyword=keyword, subword="pyodbc")
    extension.cache = cache.MemoryCache(max_age=cache_maxage, min_cost=2)
    register_extension(extension)
