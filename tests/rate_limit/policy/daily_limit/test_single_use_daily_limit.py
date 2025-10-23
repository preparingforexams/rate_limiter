import pytest

from rate_limiter import RateLimitingPolicy
from rate_limiter.policy.daily_limit import DailyLimitRateLimitingPolicy


@pytest.fixture()
def policy() -> RateLimitingPolicy:
    return DailyLimitRateLimitingPolicy(limit=1)


@pytest.mark.asyncio
async def test_get_offending_usages_no_usages(policy, now):
    offending_usage = await policy.get_offending_usage(at_time=now, last_usages=[])
    assert offending_usage is None


@pytest.mark.asyncio
async def test_get_offending_usages_too_many_usages(
    policy,
    create_usage,
    now,
    yesterday,
    earlier_today,
    tomorrow,
):
    with pytest.raises(ValueError):
        await policy.get_offending_usage(
            at_time=now,
            last_usages=[create_usage(time) for time in [yesterday, earlier_today]],
        )


@pytest.mark.asyncio
async def test_get_offending_usages_yesterday(policy, now, create_usage, yesterday):
    usage = create_usage(yesterday)
    offending_usage = await policy.get_offending_usage(at_time=now, last_usages=[usage])
    assert offending_usage is None


@pytest.mark.asyncio
async def test_get_offending_usages_tomorrow(policy, now, create_usage, tomorrow):
    usage = create_usage(tomorrow)
    offending_usage = await policy.get_offending_usage(at_time=now, last_usages=[usage])
    assert offending_usage is None


@pytest.mark.asyncio
async def test_get_offending_usages_earlier_today(
    policy, now, create_usage, earlier_today
):
    usage = create_usage(earlier_today)
    offending_usage = await policy.get_offending_usage(at_time=now, last_usages=[usage])
    assert offending_usage is usage


@pytest.mark.asyncio
async def test_get_offending_usages_later_today(policy, now, create_usage, later_today):
    # This one might seem dumb, but DST exists
    usage = create_usage(later_today)
    offending_usage = await policy.get_offending_usage(at_time=now, last_usages=[usage])
    assert offending_usage is usage
