from typing import Annotated, List
from fastapi import APIRouter, File, UploadFile
from app.services.document_service import doc_processed_payload

router = APIRouter(tags=["upload_doc"])

@router.post("/upload_doc", summary="Upload documents")
async def upload_docs(
    files: List[UploadFile] = File(...)
):
    """Upload a minimum 3 and maximum 5 files"""
    result = await doc_processed_payload(files)
    return result