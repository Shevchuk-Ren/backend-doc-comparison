from typing import List
from fastapi import APIRouter, File, UploadFile, Depends, Request
from app.core.orchestrator import orchestrator, history_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_sesion
from .users import get_current_user, optional_user
from app.schemas.user_schema import UserOut
from app.schemas.history_schema import HistoryItemOut
from app.core.rate_limit import limiter

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/analysis")
@limiter.limit("3/minute")
async def analysis_documents(
    request: Request,
    files: List[UploadFile] = File(...),
    current_user: UserOut | None = Depends(optional_user),
    db: AsyncSession = Depends(get_sesion),
):

    result = await orchestrator.process_documents(files, current_user, db)
    return result


@router.get("/history")
async def get_history(
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_sesion),
):
    return await history_service.get_history_list(db=db, user_id=current_user.id)


@router.get("/history/{history_id}", response_model=HistoryItemOut)
async def get_history_item(
    history_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_sesion),
):
    return await history_service.get_history_item(
        db=db, history_id=history_id, user_id=current_user.id
    )
