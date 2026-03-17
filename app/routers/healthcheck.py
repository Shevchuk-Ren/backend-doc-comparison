from fastapi import APIRouter, Depends
from app.schemas.healthcheck_schema import HealthCheckResp
from app.services.healthcheck_service import get_healthcheck_payload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_sesion
from sqlalchemy import text

router = APIRouter(tags=["healthcheck"])


@router.get("/", summary="Health check")
def healthcheck() -> HealthCheckResp:
    return HealthCheckResp(**get_healthcheck_payload())


@router.get("/postgres/healthcheck", summary="BD healthcheck")
async def postgres_healthcheck(
    db: AsyncSession = Depends(get_sesion),
):
    result = await db.execute(text("SELECT 1"))
    value = result.scalar_one()
    return {"postgres": "ok", "result": value}
