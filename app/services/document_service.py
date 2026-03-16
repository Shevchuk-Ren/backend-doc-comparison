from fastapi import HTTPException, UploadFile, status
from app.validators.document_validator import DocumentValidator
from .document_parser import DocumentParser
from .ollama_service import OllamaService
import json
from app.prompts.document_summary import SYSTEM_PROMPT, build_document_prompt
from .comparison_service import ComparisonService


class DocumentService:
    def __init__(self):
        self.validator = DocumentValidator()
        self.parser = DocumentParser()
        self.ollama_service = OllamaService()
        self.comparison_service = ComparisonService()

    async def process_documents(self, files: list[UploadFile]) -> dict:
        if len(files) < 2 or len(files) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You must upload from 2 to 5 documents.",
            )

        parsed_files = []

        for file in files:
            validation = await self.validator.validate_file(file)

            if not validation["valid"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"filename": file.filename, "errors": validation["errors"]},
                )

            parsed = await self.parser.parse(file)
            parsed["size"] = validation["size"]

            summary = await self.ollama_service.chat(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=build_document_prompt(parsed["text"]),
            )
            try:
                summary_data = json.loads(summary)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Invalid JSON returned by LLM for file {file.filename}",
                )

            parsed["summary"] = summary_data
            parsed_files.append(parsed)

        table = self.comparison_service.comparison_table(parsed_files)

        return {"documents": parsed_files, **table}
