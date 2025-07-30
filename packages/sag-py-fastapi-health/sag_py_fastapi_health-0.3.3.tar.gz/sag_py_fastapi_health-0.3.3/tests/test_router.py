import json
from typing import Any, Literal, cast

import pytest
from fastapi import Response
from fastapi.routing import APIRoute

from sag_py_fastapi_health.formatter import DefaultResponseFormatter
from sag_py_fastapi_health.models import Check, CheckResult, Probe
from sag_py_fastapi_health.router import HealthcheckRouter


def test__add_probe_route() -> None:
    # Arrange
    probe_one = Probe(name="probe1", checks=[], summary="A summary - 1", response_formatter=DefaultResponseFormatter())
    probe_two = Probe(name="probe2", checks=[], response_formatter=DefaultResponseFormatter())
    probe_three = Probe(name="probe_three - test", checks=[], response_formatter=DefaultResponseFormatter())

    # Act
    router = HealthcheckRouter(probe_one, probe_two, probe_three)

    # Assert
    route_one: APIRoute = cast(APIRoute, router.routes[0])
    assert route_one.path == "/probe1"
    assert route_one.summary == "A summary - 1"
    assert route_one.unique_id == "handle_request_probe1_get"

    route_two: APIRoute = cast(APIRoute, router.routes[1])
    assert route_two.path == "/probe2"
    assert route_two.summary == "Probe2 probe"
    assert route_two.unique_id == "handle_request_probe2_get"

    route_three: APIRoute = cast(APIRoute, router.routes[2])
    assert route_three.path == "/probe_three - test"
    assert route_three.summary == "Probe three test probe"
    assert route_three.unique_id == "handle_request_probe_three___test_get"


class TestCheck(Check):
    __test__ = False  # Avoid warning in unit test run

    def __init__(self, name: str = "check", is_healthy: bool = True, is_degraded: bool = False) -> None:
        self._name: str = name
        self._is_healthy: bool = is_healthy
        self._is_degraded: bool = is_degraded

    async def __call__(self) -> CheckResult:
        healthy_or_degraded: Literal["Healthy", "Degraded"] = "Degraded" if self._is_degraded else "Healthy"
        return CheckResult(
            name=self._name,
            status=healthy_or_degraded if self._is_healthy else "Unhealthy",
            description="Check was running",
        )


@pytest.mark.asyncio(loop_scope="function")
async def test__handle_request() -> None:
    # Arrange
    checks: list[Check] = [TestCheck("checkOne"), TestCheck("checkTwo")]
    probe_one = Probe(name="probe1", checks=checks, summary="A summary", response_formatter=DefaultResponseFormatter())
    router = HealthcheckRouter(probe_one)

    # Act
    response: Response = await router._handle_request(probe_one)

    # Assert
    result: Any = json.loads(response.body)
    assert result["status"] == "Healthy"

    first_result: Any = result["entries"][0]
    assert first_result["name"] == "checkOne"
    assert first_result["status"] == "Healthy"
    assert first_result["description"] == "Check was running"

    second_result: Any = result["entries"][0]
    assert second_result["name"] == "checkOne"
    assert second_result["status"] == "Healthy"
    assert second_result["description"] == "Check was running"


@pytest.mark.asyncio(loop_scope="function")
async def test__handle_request__with_failing_check() -> None:
    # Arrange
    checks: list[Check] = [TestCheck("checkOne"), TestCheck("checkTwo", is_healthy=False)]
    probe_one = Probe(name="probe1", checks=checks, summary="A summary", response_formatter=DefaultResponseFormatter())
    router = HealthcheckRouter(probe_one)

    # Act
    response: Response = await router._handle_request(probe_one)

    # Assert
    result: Any = json.loads(response.body)
    assert result["status"] == "Unhealthy"

    first_result: Any = result["entries"][0]
    assert first_result["name"] == "checkOne"
    assert first_result["status"] == "Healthy"
    assert first_result["description"] == "Check was running"

    second_result: Any = result["entries"][1]
    assert second_result["name"] == "checkTwo"
    assert second_result["status"] == "Unhealthy"
    assert second_result["description"] == "Check was running"


@pytest.mark.asyncio(loop_scope="function")
async def test__handle_request__with_degraded_check() -> None:
    # Arrange
    checks: list[Check] = [TestCheck("checkOne"), TestCheck("checkTwo", is_degraded=True)]
    probe_one = Probe(name="probe1", checks=checks, summary="A summary", response_formatter=DefaultResponseFormatter())
    router = HealthcheckRouter(probe_one)

    # Act
    response: Response = await router._handle_request(probe_one)

    # Assert
    result: Any = json.loads(response.body)
    assert result["status"] == "Degraded"

    first_result: Any = result["entries"][0]
    assert first_result["name"] == "checkOne"
    assert first_result["status"] == "Healthy"
    assert first_result["description"] == "Check was running"

    second_result: Any = result["entries"][1]
    assert second_result["name"] == "checkTwo"
    assert second_result["status"] == "Degraded"
    assert second_result["description"] == "Check was running"
