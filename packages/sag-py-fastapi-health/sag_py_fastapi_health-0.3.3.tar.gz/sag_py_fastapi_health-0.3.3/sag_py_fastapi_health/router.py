import asyncio
import datetime
from typing import Any, Coroutine, Literal, cast

from fastapi import APIRouter, Response

from sag_py_fastapi_health.models import Check, CheckResult, HealthcheckReport, Probe


class HealthcheckRouter(APIRouter):
    def __init__(self, *probes: Probe) -> None:
        super().__init__(tags=["Healthchecks"])
        for probe in probes:
            self._add_probe_route(probe)

    def _add_probe_route(self, probe: Probe) -> None:
        async def handle_request() -> Response:
            return await self._handle_request(probe)  # pragma: no cover

        self.add_api_route(
            path=f"/{probe.name}",
            endpoint=handle_request,
            response_model=probe.response_formatter.get_response_type(),
            summary=probe.endpoint_summary,
            include_in_schema=probe.include_in_schema,
        )

    async def _handle_request(self, probe: Probe) -> Response:
        tasks: list[Coroutine[Any, Any, CheckResult]] = [self._run_check(check) for check in probe.checks]
        results: list[CheckResult] = cast(list[CheckResult], await asyncio.gather(*tasks))

        total_duration: float = sum(result.duration for result in results)
        status: Literal["Unhealthy", "Degraded", "Healthy"] = self._get_total_status(results)
        report = HealthcheckReport(status=status, entries=results, total_duration=total_duration)

        return probe.response_formatter.format(report)

    async def _run_check(self, check: Check) -> CheckResult:
        start_time = datetime.datetime.now()
        check_result: CheckResult = await check()
        elapsed = datetime.datetime.now() - start_time
        check_result.duration = int(elapsed.total_seconds() * 1000)
        return check_result

    def _get_total_status(self, results: list[CheckResult]) -> Literal["Unhealthy", "Degraded", "Healthy"]:
        status: Literal["Unhealthy", "Degraded", "Healthy"] = "Healthy"
        if any(result.status == "Unhealthy" for result in results):
            status = "Unhealthy"
        elif any(result.status == "Degraded" for result in results):
            status = "Degraded"
        return status
