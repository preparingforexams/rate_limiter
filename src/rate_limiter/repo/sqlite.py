import logging
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Self

from .. import RateLimitingRepo, Usage

_LOG = logging.getLogger(__name__)


class SqliteRateLimitingRepo(RateLimitingRepo):
    def __init__(self, connection: sqlite3.Connection):
        try:
            from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor

            connection = SQLite3Instrumentor().instrument_connection(
                connection,
            )
        except ImportError:
            _LOG.info("Not instrumenting sqlite3 connection")

        self._connection = connection

    @classmethod
    def connect(cls, db_file: Path) -> Self:
        if db_file.exists() and not db_file.is_file():
            raise ValueError(f"Database file {db_file} exists and is not a file")
        connection = sqlite3.connect(db_file)
        return cls(connection)

    @contextmanager
    def _cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        cursor = self._connection.cursor()
        try:
            yield cursor
            cursor.connection.commit()
        finally:
            cursor.close()

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
                VALUES (?, ?, ?, ?, ?);
                """,
                [
                    context_id,
                    user_id,
                    int(utc_time.timestamp()),
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
                WHERE context_id = ? AND user_id = ?
                ORDER BY time DESC
                LIMIT ?
                """,
                [context_id, user_id, limit],
            )
            usages = [
                Usage(
                    context_id=context_id,
                    user_id=user_id,
                    time=datetime.fromtimestamp(row[0], tz=UTC),
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
                WHERE time < ?
                """,
                [until.timestamp()],
            )

    def close(self) -> None:
        self._connection.close()
