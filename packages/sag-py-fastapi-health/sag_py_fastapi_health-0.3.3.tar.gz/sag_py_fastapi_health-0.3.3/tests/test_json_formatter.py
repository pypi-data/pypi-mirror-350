from fastapi import Response
from pydantic import BaseModel

from sag_py_fastapi_health.formatter import DefaultResponseFormatter
from sag_py_fastapi_health.models import CheckResult, HealthcheckReport


def test__prtg_response_formatter__response_type() -> None:
    # Act
    actual: type[BaseModel] = DefaultResponseFormatter().get_response_type()

    # Assert
    assert actual == HealthcheckReport


def test__json_response_formatter__healthy() -> None:
    # Arrange
    check_results: list[CheckResult] = [
        CheckResult(name="checkOne", status="Healthy", duration=50, description="Check ok"),
        CheckResult(name="checkTwo", status="Healthy", duration=50, description="Check ok"),
    ]
    health_check_report = HealthcheckReport(status="Healthy", total_duration=100, entries=check_results)

    # Act
    actual: Response = DefaultResponseFormatter().format(health_check_report)

    # Assert
    assert actual.status_code == 200
    assert (
        actual.body == b'{"status":"Healthy","total_duration":100.0,'
        b'"entries":[{"name":"checkOne","status":"Healthy","duration":50.0,"description":"Check ok"},'
        b'{"name":"checkTwo","status":"Healthy","duration":50.0,"description":"Check ok"}]}'
    )


def test__json_response_formatter__unhealthy() -> None:
    # Arrange
    check_results: list[CheckResult] = [
        CheckResult(name="checkOne", status="Unhealthy", duration=50, description="Something failed"),
        CheckResult(name="checkTwo", status="Healthy", duration=50, description="Check ok"),
    ]
    health_check_report = HealthcheckReport(status="Unhealthy", total_duration=100, entries=check_results)

    # Act
    actual: Response = DefaultResponseFormatter().format(health_check_report)

    # Assert
    assert actual.status_code == 503
    assert (
        actual.body == b'{"status":"Unhealthy","total_duration":100.0,'
        b'"entries":[{"name":"checkOne","status":"Unhealthy","duration":50.0,"description":"Something failed"},'
        b'{"name":"checkTwo","status":"Healthy","duration":50.0,"description":"Check ok"}]}'
    )
