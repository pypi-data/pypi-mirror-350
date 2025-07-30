from fastapi import Response
from pydantic import BaseModel

from sag_py_fastapi_health.formatter import PrtgReport, PrtgResponseFormatter
from sag_py_fastapi_health.models import CheckResult, HealthcheckReport


def test__prtg_response_formatter__response_type() -> None:
    # Act
    actual: type[BaseModel] = PrtgResponseFormatter().get_response_type()

    # Assert
    assert actual == PrtgReport


def test__prtg_response_formatter__healthy() -> None:
    # Arrange
    check_results: list[CheckResult] = [
        CheckResult(name="checkOne", status="Healthy", duration=50, description="Check ok"),
        CheckResult(name="checkTwo", status="Healthy", duration=50, description="Check ok"),
    ]
    health_check_report = HealthcheckReport(status="Healthy", total_duration=100, entries=check_results)

    # Act
    actual: Response = PrtgResponseFormatter().format(health_check_report)

    # Assert
    assert actual.status_code == 200
    assert (
        actual.body == b'{"prtg":{"error":0,"text":"","result":[{"value":100.0,"channel":"TotalDuration","float":true,'
        b'"unit":"TimeResponse"},{"value":50.0,"channel":"checkOne.Duration","float":true,"unit":"TimeResponse"},'
        b'{"value":50.0,"channel":"checkTwo.Duration","float":true,"unit":"TimeResponse"}]}}'
    )


def test__prtg_response_formatter__unhealthy() -> None:
    # Arrange
    check_results: list[CheckResult] = [
        CheckResult(name="checkOne", status="Unhealthy", duration=50, description="Something failed"),
        CheckResult(name="checkTwo", status="Healthy", duration=50, description="Check ok"),
    ]
    health_check_report = HealthcheckReport(status="Unhealthy", total_duration=100, entries=check_results)

    # Act
    actual: Response = PrtgResponseFormatter().format(health_check_report)

    # Assert
    assert actual.status_code == 200
    assert (
        actual.body
        == b'{"prtg":{"error":1,"text":"checkOne: Something failed","result":[{"value":100.0,"channel":"TotalDuration"'
        b',"float":true,"unit":"TimeResponse"},{"value":50.0,"channel":"checkOne.Duration","float":true,'
        b'"unit":"TimeResponse"},{"value":50.0,"channel":"checkTwo.Duration","float":true,"unit":"TimeResponse"}]}}'
    )
