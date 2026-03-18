from app.schemas.ollama_schema import DocumentSummaryLLM
from fastapi import HTTPException, status
import json
from app.prompts.document_summary import SYSTEM_PROMPT, build_document_prompt
from pydantic import ValidationError


class SummaryService:
    def __init__(self, llm_service):
        self.llm = llm_service

    async def generate(self, text: str) -> DocumentSummaryLLM:
        raw = await self.llm.chat(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_document_prompt(text),
        )
        return self._parse_summary_response(raw)

    def _parse_summary_response(self, raw: str) -> DocumentSummaryLLM:
        if not raw or not raw.strip():
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="LLM returned empty response for summary",
            )

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="LLM returned invalid JSON for summary",
            )

        try:
            return DocumentSummaryLLM.model_validate(data)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="LLM returned JSON with invalid summary schema",
            )
