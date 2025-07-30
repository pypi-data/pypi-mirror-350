import re
from abc import ABC, abstractmethod
from typing import Iterable, Literal, NamedTuple

from fastapi import Response
from pydantic import BaseModel


class CheckResult(BaseModel):
    name: str
    status: Literal["Healthy", "Unhealthy", "Degraded"]
    duration: float = 0
    description: str | None = None


class Check(ABC):
    @abstractmethod
    async def __call__(self) -> CheckResult: ...  # pragma: no cover


class HealthcheckReport(BaseModel):
    status: Literal["Healthy", "Unhealthy", "Degraded"]
    total_duration: float
    entries: list[CheckResult]


class HealthResponseFormatter:
    @abstractmethod
    def get_response_type(self) -> type[BaseModel]:
        pass  # pragma: no cover

    @abstractmethod
    def format(self, report: HealthcheckReport) -> Response:
        pass  # pragma: no cover


class Probe(NamedTuple):
    name: str
    checks: Iterable[Check]
    response_formatter: HealthResponseFormatter
    summary: str | None = None
    include_in_schema: bool = True

    @property
    def endpoint_summary(self) -> str:
        if self.summary:
            return self.summary

        title: str = re.sub(
            pattern=r"[^a-z0-9]+",
            repl=" ",
            string=self.name.lower().capitalize(),
            flags=re.IGNORECASE,
        )
        return f"{title} probe"
