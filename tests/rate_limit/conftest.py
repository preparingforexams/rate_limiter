from datetime import datetime, timedelta, tzinfo
from zoneinfo import ZoneInfo

import pytest


@pytest.fixture()
def timezone() -> tzinfo:
    return ZoneInfo("Europe/Berlin")


@pytest.fixture()
def now(timezone) -> datetime:
    return datetime.now(timezone)


@pytest.fixture()
def earlier_today(timezone) -> datetime:
    return datetime.now(timezone) - timedelta(minutes=1)


@pytest.fixture()
def later_today(timezone) -> datetime:
    result = datetime.now(timezone) + timedelta(minutes=1)
    return result


@pytest.fixture()
def yesterday(timezone) -> datetime:
    yesterday_exact: datetime = datetime.now(timezone) - timedelta(days=1)
    result = yesterday_exact.replace(
        hour=23,
        minute=59,
        second=33,
        microsecond=0,
    )
    return result


@pytest.fixture()
def tomorrow(timezone) -> datetime:
    yesterday_exact = datetime.now(timezone) + timedelta(days=1)
    result = yesterday_exact.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    return result
