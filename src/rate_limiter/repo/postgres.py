import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Self

import psycopg
import psycopg_pool

from .. import RateLimitingRepo, Usage

_LOG = logging.getLogger(__name__)


class PostgresRateLimitingRepo(RateLimitingRepo):
    def __init__(
        self,
        connection_pool: psycopg_pool.AsyncConnectionPool[psycopg.AsyncConnection],
    ):
        self._pool = connection_pool

    @staticmethod
    def _instrument_psycopg() -> None:
        try:
            from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
        except ImportError:
            _LOG.info("Not instrumenting postgres connections")
            return None

        PsycopgInstrumentor().instrument()

    @classmethod
    async def connect(
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
        cls._instrument_psycopg()

        pool = psycopg_pool.AsyncConnectionPool(
            conninfo=f"postgresql://{username}:{password}@{host}:{port}/{database}",
            min_size=min_connections,
            max_size=max_connections,
            open=False,
        )

        await pool.open(wait=True)

        async with pool.connection() as connection:
            await pool.check_connection(connection)

        return cls(pool)

    @asynccontextmanager
    async def _cursor(self) -> AsyncGenerator[psycopg.AsyncCursor, None]:
        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                yield cursor

    async def add_usage(
        self,
        *,
        context_id: str,
        user_id: str,
        utc_time: datetime,
        reference_id: str | None,
        response_id: str | None,
    ):
        async with self._cursor() as cursor:
            await cursor.execute(
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

    async def get_usages(
        self,
        *,
        context_id: str,
        user_id: str,
        limit: int = 1,
    ) -> list[Usage]:
        async with self._cursor() as cursor:
            result = await cursor.execute(
                """
                SELECT time, reference_id, response_id FROM usages
                WHERE context_id = %s AND user_id = %s
                ORDER BY time DESC
                LIMIT %s
                """,
                [context_id, user_id, limit],
            )

            usages = []
            async for row in result:
                usage = Usage(
                    context_id=context_id,
                    user_id=user_id,
                    time=row[0],
                    reference_id=row[1],
                    response_id=row[2],
                )
                usages.append(usage)

        _LOG.debug(
            "Found %d usages for user %s in context %s (limit was %d)",
            len(usages),
            user_id,
            context_id,
            limit,
        )

        return usages

    async def drop_old_usages(self, *, until: datetime) -> None:
        async with self._cursor() as cursor:
            await cursor.execute(
                """
                DELETE FROM usages
                WHERE time < %s
                """,
                [until],
            )

    async def close(self) -> None:
        await self._pool.close()
