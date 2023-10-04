from datetime import datetime
from typing import Callable

import pytest

from rate_limit import Usage


@pytest.fixture()
def create_usage() -> Callable[[datetime], Usage]:
    id_counter = 0

    def _create_usage(time: datetime) -> Usage:
        nonlocal id_counter
        current_id = id_counter
        id_counter += 1
        return Usage(
            context_id=f"test-context-{current_id}",
            user_id=f"test-user-{current_id}",
            time=time,
            reference_id=f"reference-{current_id}",
            response_id=f"response-{current_id}",
        )

    return _create_usage
