from fastapi import HTTPException, UploadFile
import json
from app.prompts.document_summary import SYSTEM_PROMPT, build_document_prompt


class DocumentOrchestrator:
    def __init__(self, document_service, llm, comparison_service, decision_service):
        self.document_service = document_service
        self.llm = llm
        self.comparison_service = comparison_service
        self.decision_service = decision_service

    async def process_documents(self, files: list[UploadFile]) -> dict:
        if not 2 <= len(files) <= 5:
            raise HTTPException(
                status_code=400,
                detail="You must upload from 2 to 5 documents.",
            )

        parsed_files = []
        for file in files:
            parsed = await self.document_service.process_single(file)

            summary_raw = await self.llm.chat(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=build_document_prompt(parsed["text"]),
            )

            parsed["summary"] = json.loads(summary_raw)
            parsed_files.append(parsed)

        table = self.comparison_service.comparison_table(parsed_files)
        goals = await self.decision_service.goal_analysis(parsed_files, table)

        return {
            "documents": parsed_files,
            **table,
            **goals,
        }
