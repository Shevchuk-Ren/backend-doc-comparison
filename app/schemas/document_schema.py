from pydantic import BaseModel


class ComparisonResult(BaseModel):
    documents: list[dict]
    comparison_table: list[dict]
    goals: list[dict]
