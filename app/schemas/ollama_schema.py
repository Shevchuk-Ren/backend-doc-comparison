from pydantic import BaseModel
from typing import List


class DocumentSummaryLLM(BaseModel):
    document_type: str
    main_purpose: str
    key_points: List[str]
    pros: List[str]
    cons: List[str]
    risk_flags: List[str]
