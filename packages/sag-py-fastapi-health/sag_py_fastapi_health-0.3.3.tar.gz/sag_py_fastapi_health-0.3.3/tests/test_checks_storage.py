import pytest

from sag_py_fastapi_health.checks.storage import StorageExistsCheck, StorageReadableCheck, StorageWritableCheck
from sag_py_fastapi_health.models import CheckResult


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageExistsCheck__ignore_unconfigured() -> None:
    # Act
    check: CheckResult = await StorageExistsCheck("", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Healthy"
    assert check.description == "Empty path"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageExistsCheck__error_on_empty() -> None:
    # Act
    check: CheckResult = await StorageExistsCheck("", "myStorageCheck", False)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Unhealthy"
    assert check.description == "Empty path"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageExistsCheck__path_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("os.path.isdir", lambda path: True)

    # Act
    check: CheckResult = await StorageExistsCheck("/existing/path", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Healthy"
    assert check.description == "Path exists"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageExistsCheck__path_not_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("os.path.isdir", lambda path: False)

    # Act
    check: CheckResult = await StorageExistsCheck("/existing/path", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Unhealthy"
    assert check.description == "Path '/existing/path' does not exist or isn't a directory"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageReadableCheck__ignore_unconfigured() -> None:
    # Act
    check: CheckResult = await StorageReadableCheck("", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Healthy"
    assert check.description == "Empty path"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageReadableCheck__error_on_empty() -> None:
    # Act
    check: CheckResult = await StorageReadableCheck("", "myStorageCheck", False)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Unhealthy"
    assert check.description == "Empty path"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageReadableCheck__path_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("os.access", lambda path, mode: True)

    # Act
    check: CheckResult = await StorageReadableCheck("/existing/path", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Healthy"
    assert check.description == "Path readable"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageReadableCheck__path_not_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("os.access", lambda path, mode: False)

    # Act
    check: CheckResult = await StorageReadableCheck("/existing/path", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Unhealthy"
    assert check.description == "Path '/existing/path' not readable"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageWritableCheck__ignore_unconfigured() -> None:
    # Act
    check: CheckResult = await StorageWritableCheck("", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Healthy"
    assert check.description == "Empty path"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageWritableCheck__error_on_empty() -> None:
    # Act
    check: CheckResult = await StorageWritableCheck("", "myStorageCheck", False)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Unhealthy"
    assert check.description == "Empty path"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageWritableCheck__path_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("os.access", lambda path, mode: True)

    # Act
    check: CheckResult = await StorageWritableCheck("/existing/path", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Healthy"
    assert check.description == "Path writable"


@pytest.mark.asyncio(loop_scope="function")
async def test__StorageWritableCheck__path_not_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("os.access", lambda path, mode: False)

    # Act
    check: CheckResult = await StorageWritableCheck("/existing/path", "myStorageCheck", True)()

    # Assert
    assert check.name == "myStorageCheck"
    assert check.status == "Unhealthy"
    assert check.description == "Path '/existing/path' not writable"
