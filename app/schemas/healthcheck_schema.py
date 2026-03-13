from pydantic import BaseModel
from fastapi import APIRouter, File, UploadFile


class HealthCheckResp(BaseModel):
    status_code: int
    detail: str
    result: str

class DocProcessedRequest(BaseModel):
    files: list[UploadFile]