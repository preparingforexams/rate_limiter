import logging
from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import datetime
from typing import Self

import psycopg
import psycopg_pool

from .. import RateLimitingRepo, Usage

_LOG = logging.getLogger(__name__)


class PostgresRateLimitingRepo(RateLimitingRepo):
    def __init__(
        self,
        connection_pool: psycopg_pool.ConnectionPool[psycopg.Connection],
    ):
        self._pool = connection_pool

    @staticmethod
    def _get_connection_configurator() -> Callable[[psycopg.Connection], None] | None:
        try:
            from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
        except ImportError:
            _LOG.info("Not instrumenting postgres connections")
            return None

        def _configure_connection(connection: psycopg.Connection) -> None:
            PsycopgInstrumentor.instrument_connection(connection)

        return _configure_connection

    @classmethod
    def connect(
        cls,
        *,
        host: str,
        port: int = 5432,
        database: str,
        username: str,
        password: str,
        min_connections: int = 2,
        max_connections: int = 10,
    ) -> Self:
        pool = psycopg_pool.ConnectionPool(
            conninfo=f"postgresql://{username}:{password}@{host}:{port}/{database}",
            configure=cls._get_connection_configurator(),
            min_size=min_connections,
            max_size=max_connections,
            open=True,
        )

        with pool.connection() as connection:
            pool.check_connection(connection)

        return cls(pool)

    @contextmanager
    def _cursor(self) -> Generator[psycopg.Cursor, None, None]:
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                yield cursor

    def add_usage(
        self,
        *,
        context_id: str,
        user_id: str,
        utc_time: datetime,
        reference_id: str | None,
        response_id: str | None,
    ):
        with self._cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usages (
                    context_id,
                    user_id,
                    time,
                    reference_id,
                    response_id
                )
                VALUES (%s, %s, %s, %s, %s);
                """,
                [
                    context_id,
                    user_id,
                    utc_time,
                    reference_id,
                    response_id,
                ],
            )
        _LOG.debug("Inserted usage for user %s in context %s", user_id, context_id)

    def get_usages(
        self,
        *,
        context_id: str,
        user_id: str,
        limit: int = 1,
    ) -> list[Usage]:
        with self._cursor() as cursor:
            result = cursor.execute(
                """
                SELECT time, reference_id, response_id FROM usages
                WHERE context_id = %s AND user_id = %s
                ORDER BY time DESC
                LIMIT %s
                """,
                [context_id, user_id, limit],
            )
            usages = [
                Usage(
                    context_id=context_id,
                    user_id=user_id,
                    time=row[0],
                    reference_id=row[1],
                    response_id=row[2],
                )
                for row in result
            ]

        _LOG.debug(
            "Found %d usages for user %s in context %s (limit was %d)",
            len(usages),
            user_id,
            context_id,
            limit,
        )

        return usages

    def drop_old_usages(self, *, until: datetime) -> None:
        with self._cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM usages
                WHERE time < %s
                """,
                [until],
            )

    def close(self) -> None:
        self._pool.close()
