# type: ignore
import mock
import pytest
from aiohttp import ClientResponse
from aiohttp.helpers import TimerNoop
from yarl import URL

from sag_py_fastapi_health.checks.http import HttpCheck
from sag_py_fastapi_health.models import CheckResult


@pytest.mark.asyncio(loop_scope="function")
async def test__HttpCheck__with_ok_result(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    response = ClientResponse(
        "get",
        URL("http://localhost/test"),
        request_info=mock.Mock(),
        writer=None,  # type: ignore [arg-type]
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=mock.Mock(),
        session=mock.Mock(),
    )
    response.status = 200
    monkeypatch.setattr("aiohttp.ClientSession.get", lambda self, url: response)

    # Act
    check: CheckResult = await HttpCheck("http://localhost/test", name="myHttpCheck")()

    # Assert
    assert check.name == "myHttpCheck"
    assert check.status == "Healthy"
    assert check.description == "Got status 200"


@pytest.mark.asyncio(loop_scope="function")
async def test__HttpCheck__with_no_content_result(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    response = ClientResponse(
        "get",
        URL("http://localhost/test"),
        request_info=mock.Mock(),
        writer=None,  # type: ignore [arg-type]
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=mock.Mock(),
        session=mock.Mock(),
    )
    response.status = 204
    monkeypatch.setattr("aiohttp.ClientSession.get", lambda self, url: response)

    # Act
    check: CheckResult = await HttpCheck("http://localhost/test", name="myHttpCheck")()

    # Assert
    assert check.name == "myHttpCheck"
    assert check.status == "Healthy"
    assert check.description == "Got status 204"


@pytest.mark.asyncio(loop_scope="function")
async def test__HttpCheck__with_error_result(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    response = ClientResponse(
        "get",
        URL("http://localhost/test"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=mock.Mock(),
        session=mock.Mock(),
    )
    response.status = 500
    monkeypatch.setattr("aiohttp.ClientSession.get", lambda self, url: response)

    # Act
    check: CheckResult = await HttpCheck("http://localhost/test", name="myHttpCheck")()

    # Assert
    assert check.name == "myHttpCheck"
    assert check.status == "Unhealthy"
