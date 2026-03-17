from pydantic import BaseModel


class ComparisonOut(BaseModel):
    table: list
    decision_summary: dict


class DocumentSummaryOut(BaseModel):
    document_type: str
    main_purpose: str
    key_points: list
    pros: list
    cons: list
    risk_flags: list


class DocumentOut(BaseModel):
    id: int
    filename: str
    preview: str
    summary: DocumentSummaryOut
