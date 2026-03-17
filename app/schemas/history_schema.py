from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .document_schema import DocumentOut, ComparisonOut


class HistoryListItem(BaseModel):
    id: int
    created_at: datetime
    filenames: List[str]
    decision_summary: Optional[str]
    result_id: int

    class Config:
        orm_mode = True


class HistoryItemOut(BaseModel):
    documents: List[DocumentOut]
    comparison: ComparisonOut
