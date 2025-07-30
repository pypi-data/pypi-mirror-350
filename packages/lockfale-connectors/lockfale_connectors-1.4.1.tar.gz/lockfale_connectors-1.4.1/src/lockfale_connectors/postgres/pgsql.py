import logging.config
from typing import Any, Dict, List, Optional

import pandas as pd
import psycopg
from psycopg.errors import DatabaseError
from psycopg.rows import dict_row

from . import config

logging.config.fileConfig("log.ini")
logger = logging.getLogger("console")
logger.setLevel(logging.INFO)


class PostgreSQLConnectionError(Exception):
    pass


class DuplicateKeyException(Exception):
    pass


class PostgreSQLConnector:
    """
    PostgreSQL Connector using psycopg (v3) with direct connections.
    Let PgBouncer handle pooling on the DB side.
    """

    def __init__(self, retries=3):
        self._retries = retries

    def _get_connection(self):
        """Establish a direct PostgreSQL connection."""
        try:
            conn = psycopg.connect(
                f"postgresql://{config.PGDBSettingsFromEnvironmentAdmin().db_user}:"
                f"{config.PGDBSettingsFromEnvironmentAdmin().db_password}@"
                f"{config.PGDBSettingsFromEnvironmentAdmin().db_host}:"
                f"{config.PGDBSettingsFromEnvironmentAdmin().db_port}/"
                f"{config.PGDBSettingsFromEnvironmentAdmin().db_database}"
                "?sslmode=require",
                row_factory=dict_row
            )
            logger.info("PostgreSQL direct connection established.")
            return conn
        except Exception as e:
            logger.error(f"Error establishing PostgreSQL connection: {e}")
            raise PostgreSQLConnectionError(e)

    def execute(self, query: str, params: Dict[str, Any] = None) -> Optional[int]:
        """Execute a single SQL query."""
        available_calls = self._retries
        while available_calls > 0:
            try:
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params)
                        conn.commit()

                        # Return the ID if it's an insert
                        if "insert into" in query.lower() and "returning id" in query.lower():
                            if cursor.rowcount > 0:
                                return cursor.fetchone()['id']
                            return None
                        return 0  # Return zero for non-insert queries

            except DatabaseError as e:
                logger.error(f"Error executing query: {query}, Error: {e}")
                available_calls -= 1

        return -1  # Indicate failure after retries

    def execute_many(self, query: str, values: List[tuple]) -> Optional[int]:
        """Efficient batch insert/update using psycopg's execute function."""
        if not values:
            return 0  # Nothing to insert

        available_calls = self._retries
        while available_calls > 0:
            try:
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.executemany(query, values)
                        conn.commit()
                        return cursor.rowcount  # Number of rows affected

            except DatabaseError as e:
                logger.error(f"Error executing batch query: {query}, Error: {e}")
                available_calls -= 1

        return -1  # Indicate failure after retries

    def insert_many(self, query: str, values: List[tuple]) -> Optional[List[int]]:
        """Efficient batch insert/update using psycopg's execute function."""
        if not values:
            return []  # Nothing to insert

        available_calls = self._retries
        while available_calls > 0:
            try:
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.executemany(query, values)
                        ids = []
                        while True:
                            ids.append(cursor.fetchone()[0])
                            if not cursor.nextset():
                                break
                        return ids

            except DatabaseError as e:
                logger.error(f"Error executing batch query: {query}, Error: {e}")
                available_calls -= 1

        return []  # Indicate failure after retries

    def select_dataframe(self, query: str, params: Dict[str, Any] = None) -> Optional[pd.DataFrame]:
        """Execute a SELECT query and return the result as a Pandas DataFrame."""
        available_calls = self._retries
        while available_calls > 0:
            try:
                with self._get_connection() as conn:
                    return pd.read_sql_query(sql=query, con=conn, params=params)

            except DatabaseError as e:
                logger.error(f"Error executing SELECT query: {query}, Error: {e}")
                available_calls -= 1

        return None  # Return None if all retries fail

    def select_dict(self, query: str, params: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
        """Execute a SELECT query and return the result as a list of dictionaries."""
        available_calls = self._retries
        while available_calls > 0:
            try:
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params)
                        results = cursor.fetchall()
                        return results  # Returns a list of dictionaries

            except DatabaseError as e:
                logger.error(f"Error executing SELECT query: {query}, Error: {e}")
                available_calls -= 1

        return None  # Return None if all retries fail
