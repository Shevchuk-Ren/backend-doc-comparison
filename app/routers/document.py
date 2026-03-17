from typing import List
from fastapi import APIRouter, File, UploadFile
from app.core.orchestrator import orchestrator

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/analysis")
async def analysis_documents(files: List[UploadFile] = File(...)):

    result = await orchestrator.process_documents(files)
    return result
