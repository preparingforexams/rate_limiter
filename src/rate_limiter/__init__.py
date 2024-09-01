import abc
from dataclasses import dataclass
from datetime import datetime, tzinfo
from datetime import timezone as dt_timezone
from typing import Self, cast

from opentelemetry import trace
from zoneinfo import ZoneInfo

_tracer = trace.get_tracer(__name__)


@dataclass(frozen=True)
class Usage:
    context_id: str
    user_id: str
    time: datetime
    reference_id: str | None
    response_id: str | None

    def in_timezone(self, timezone: tzinfo) -> Self:
        usage = Usage(
            context_id=self.context_id,
            user_id=self.user_id,
            time=self.time.astimezone(timezone),
            reference_id=self.reference_id,
            response_id=self.response_id,
        )
        return cast(Self, usage)


class RateLimitingPolicy(abc.ABC):
    @property
    @abc.abstractmethod
    def requested_history(self) -> int:
        pass

    @abc.abstractmethod
    def get_offending_usage(
        self,
        at_time: datetime,
        last_usages: list[Usage],
    ) -> Usage | None:
        pass


class RateLimitingRepo(abc.ABC):
    @abc.abstractmethod
    def add_usage(
        self,
        context_id: str,
        user_id: str,
        utc_time: datetime,
        reference_id: str | None,
        response_id: str | None,
    ):
        pass

    @abc.abstractmethod
    def get_usages(
        self,
        context_id: str,
        user_id: str,
        limit: int = 1,
    ) -> list[Usage]:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass


class RateLimiter:
    def __init__(
        self,
        policy: RateLimitingPolicy,
        repo: RateLimitingRepo,
        timezone: tzinfo | None = None,
    ):
        self._policy = policy
        self._repo = repo
        self._timezone = timezone or ZoneInfo("Europe/Berlin")

    def get_offending_usage(
        self,
        context_id: str | int,
        user_id: str | int,
        at_time: datetime,
    ) -> Usage | None:
        with _tracer.start_as_current_span("get_offending_usage"):
            context_id = str(context_id)
            user_id = str(user_id)
            requested_history = self._policy.requested_history
            history = self._repo.get_usages(
                context_id=context_id,
                user_id=user_id,
                limit=requested_history,
            )
            return self._policy.get_offending_usage(
                at_time=at_time.astimezone(self._timezone),
                last_usages=[usage.in_timezone(self._timezone) for usage in history],
            )

    def add_usage(
        self,
        context_id: str | int,
        user_id: str | int,
        time: datetime,
        reference_id: str | None = None,
        response_id: str | None = None,
    ) -> None:
        with _tracer.start_as_current_span("add_usage"):
            context_id = str(context_id)
            user_id = str(user_id)
            utc_time = time.astimezone(dt_timezone.utc)
            self._repo.add_usage(
                context_id=context_id,
                user_id=user_id,
                utc_time=utc_time,
                reference_id=reference_id,
                response_id=response_id,
            )

    def close(self) -> None:
        self._repo.close()
