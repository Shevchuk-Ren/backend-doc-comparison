from pydantic import BaseModel


class HealthCheckResp(BaseModel):
    status_code: int
    detail: str
    result: str
