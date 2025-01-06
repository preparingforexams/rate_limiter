from datetime import datetime

from .. import RateLimitingRepo, Usage


class InMemoryRateLimitingRepo(RateLimitingRepo):
    def __init__(self) -> None:
        # TODO: this implementation should store more than one usage
        self._usage_time_by_user: dict[str, dict[str, Usage]] = {}

    def get_usages(
        self,
        *,
        context_id: str,
        user_id: str,
        limit: int = 1,
    ) -> list[Usage]:
        usage = self._usage_time_by_user.get(context_id, {}).get(user_id)
        return [usage] if usage else []

    def add_usage(
        self,
        *,
        context_id: str,
        user_id: str,
        utc_time: datetime,
        reference_id: str | None,
        response_id: str | None,
    ):
        if context_id not in self._usage_time_by_user:
            self._usage_time_by_user[context_id] = {}

        self._usage_time_by_user[context_id][user_id] = Usage(
            context_id=context_id,
            user_id=user_id,
            time=utc_time,
            reference_id=reference_id,
            response_id=response_id,
        )

    def drop_old_usages(self, *, until: datetime) -> None:
        for context in self._usage_time_by_user.values():
            old = []
            for user_id, usage in context.items():
                if usage.time < until:
                    old.append(user_id)

            for user_id in old:
                del context[user_id]

    def close(self) -> None:
        pass
