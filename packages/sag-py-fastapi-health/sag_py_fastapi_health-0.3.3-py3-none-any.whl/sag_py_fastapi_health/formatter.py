from fastapi import Response
from fastapi import status as http_status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from sag_py_fastapi_health.models import HealthcheckReport, HealthResponseFormatter


class DefaultResponseFormatter(HealthResponseFormatter):
    def get_response_type(self) -> type[BaseModel]:
        return HealthcheckReport

    def format(self, report: HealthcheckReport) -> Response:
        return JSONResponse(
            content=jsonable_encoder(report),
            status_code=(
                http_status.HTTP_200_OK if report.status == "Healthy" else http_status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )


class PrtgResult(BaseModel):
    value: float = Field(default=0)
    channel: str = Field(default="")
    float_field: bool = Field(default=True, alias="float")
    unit: str = Field(default="TimeResponse")


class PrtgResponse(BaseModel):
    error: int = Field(default=0)
    text: str = Field(default="Everything is fine :)")
    result: list[PrtgResult] = Field(default=[])


class PrtgReport(BaseModel):
    prtg: PrtgResponse = Field(default=PrtgResponse())


class PrtgResponseFormatter(HealthResponseFormatter):
    def get_response_type(self) -> type[BaseModel]:
        return PrtgReport

    def format(self, report: HealthcheckReport) -> Response:
        response_report = PrtgReport()
        response_report.prtg.error = 1 if report.status == "Unhealthy" else 0
        response_report.prtg.text = ", ".join(
            f"{entry.name}: {entry.description}"
            for entry in filter(lambda entry: entry.status == "Unhealthy", report.entries)
        )

        response_report.prtg.result.append(PrtgResult(channel="TotalDuration", value=report.total_duration))

        for entry in report.entries:
            response_report.prtg.result.append(PrtgResult(channel=f"{entry.name}.Duration", value=entry.duration))
        return JSONResponse(content=jsonable_encoder(response_report), status_code=http_status.HTTP_200_OK)
