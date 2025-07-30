import os

from sag_py_fastapi_health.models import Check, CheckResult


class StorageExistsCheck(Check):
    def __init__(self, path: str, name: str = "Storage", pass_if_unconfigured: bool = True) -> None:
        self._path: str = path
        self._name: str = name
        self._pass_if_unconfigured: bool = pass_if_unconfigured

    async def __call__(self) -> CheckResult:
        if not self._path:
            return CheckResult(
                name=self._name,
                status="Healthy" if self._pass_if_unconfigured else "Unhealthy",
                description="Empty path",
            )

        return (
            CheckResult(name=self._name, status="Healthy", description="Path exists")
            if os.path.isdir(self._path)
            else CheckResult(
                name=self._name,
                status="Unhealthy",
                description=f"Path '{self._path}' does not exist or isn't a directory",
            )
        )


class StorageReadableCheck(Check):
    def __init__(self, path: str, name: str = "Storage", pass_if_unconfigured: bool = True) -> None:
        self._path: str = path
        self._name: str = name
        self._pass_if_unconfigured: bool = pass_if_unconfigured

    async def __call__(self) -> CheckResult:
        if not self._path:
            return CheckResult(
                name=self._name,
                status="Healthy" if self._pass_if_unconfigured else "Unhealthy",
                description="Empty path",
            )

        return (
            CheckResult(name=self._name, status="Healthy", description="Path readable")
            if os.access(self._path, os.R_OK)
            else CheckResult(
                name=self._name,
                status="Unhealthy",
                description=f"Path '{self._path}' not readable",
            )
        )


class StorageWritableCheck(Check):
    def __init__(self, path: str, name: str = "Storage", pass_if_unconfigured: bool = True) -> None:
        self._path: str = path
        self._name: str = name
        self._pass_if_unconfigured: bool = pass_if_unconfigured

    async def __call__(self) -> CheckResult:
        if not self._path:
            return CheckResult(
                name=self._name,
                status="Healthy" if self._pass_if_unconfigured else "Unhealthy",
                description="Empty path",
            )

        return (
            CheckResult(name=self._name, status="Healthy", description="Path writable")
            if os.access(self._path, os.W_OK)
            else CheckResult(
                name=self._name,
                status="Unhealthy",
                description=f"Path '{self._path}' not writable",
            )
        )
