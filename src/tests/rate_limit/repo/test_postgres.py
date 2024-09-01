from datetime import datetime, timezone

import pytest

from rate_limiter import Usage
from rate_limiter.repo import PostgresRateLimitingRepo


@pytest.fixture
def repo():
    repo = PostgresRateLimitingRepo.connect(
        host="localhost",
        database="postgres",
        username="postgres",
        password="notsecret",
    )
    try:
        yield repo
    finally:
        with repo._cursor() as cursor:
            cursor.execute("TRUNCATE TABLE usages;")
        repo.close()


@pytest.mark.local
def test_no_usages(repo):
    usages = repo.get_usages("context", "user")
    assert usages == []


@pytest.mark.local
def test_add_usage(repo):
    timestamp = datetime.now(timezone.utc)
    repo.add_usage(
        context_id="context",
        user_id="user",
        utc_time=timestamp,
        reference_id="ref",
        response_id="response",
    )

    usages = repo.get_usages("context", "user")
    assert usages == [
        Usage(
            context_id="context",
            user_id="user",
            time=timestamp,
            reference_id="ref",
            response_id="response",
        )
    ]
