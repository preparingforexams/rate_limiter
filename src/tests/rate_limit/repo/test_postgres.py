from datetime import UTC, datetime

import pytest
import pytest_asyncio

from rate_limiter import Usage
from rate_limiter.repo import PostgresRateLimitingRepo


@pytest_asyncio.fixture
async def repo():
    repo = await PostgresRateLimitingRepo.connect(
        host="localhost",
        database="postgres",
        username="postgres",
        password="notsecret",
    )
    try:
        yield repo
    finally:
        async with repo._cursor() as cursor:
            await cursor.execute("TRUNCATE TABLE usages;")
        await repo.close()


@pytest.mark.local
@pytest.mark.asyncio
async def test_no_usages(repo):
    usages = await repo.get_usages(context_id="context", user_id="user")
    assert usages == []


@pytest.mark.local
@pytest.mark.asyncio
async def test_add_usage(repo):
    timestamp = datetime.now(UTC)
    await repo.add_usage(
        context_id="context",
        user_id="user",
        utc_time=timestamp,
        reference_id="ref",
        response_id="response",
    )

    usages = await repo.get_usages(context_id="context", user_id="user")
    assert usages == [
        Usage(
            context_id="context",
            user_id="user",
            time=timestamp,
            reference_id="ref",
            response_id="response",
        )
    ]
