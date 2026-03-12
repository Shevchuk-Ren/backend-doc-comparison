from fastapi import APIRouter
from app.schemas.healthcheck_schema import HealthCheckResp
from app.services.healthcheck_service import get_healthcheck_payload

router = APIRouter(tags=["healthcheck"])


@router.get("/", summary="Health check")
def healthcheck() -> HealthCheckResp:
    return HealthCheckResp(**get_healthcheck_payload())
