from typing import List
from fastapi import APIRouter, File, UploadFile
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])

document_service = DocumentService()


@router.post("/parse")
async def parse_documents(files: List[UploadFile] = File(...)):

    result = await document_service.process_documents(files)
    return result
