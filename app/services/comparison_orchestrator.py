from fastapi import HTTPException, UploadFile
import json
from app.prompts.document_summary import SYSTEM_PROMPT, build_document_prompt


class DocumentOrchestrator:
    def __init__(
        self,
        document_service,
        llm,
        comparison_service,
        decision_service,
        history_service,
    ):
        self.document_service = document_service
        self.llm = llm
        self.comparison_service = comparison_service
        self.decision_service = decision_service
        self.history_service = history_service

    async def process_documents(self, files: list[UploadFile], user, db) -> dict:
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

        if not user:
            return {
                "documents": [
                    {
                        "filename": d["filename"],
                        "preview": d["preview"],
                        "summary": d["summary"],
                    }
                    for d in parsed_files
                ],
                "comparison": {
                    "table": table["comparison_table"],
                    "decision_summary": goals["best_options"],
                },
            }

        saved_docs = []
        for f, parsed in zip(files, parsed_files):
            saved_docs.append(
                await self.document_service.save_document(
                    db=db,
                    user_id=user.id,
                    file=f,
                    preview=parsed["preview"],
                    text=parsed["text"],
                )
            )

        saved_summaries = []
        for doc, parsed in zip(saved_docs, parsed_files):
            saved_summaries.append(
                await self.document_service.save_summary(
                    db=db, document=doc, summary=parsed["summary"]
                )
            )

        saved_comparison = await self.comparison_service.save_comparison(
            db=db,
            user_id=user.id,
            documents=saved_docs,
            table=table,
            decision_summary=goals["best_options"],
        )

        await self.history_service.add(
            db=db,
            user_id=user.id,
            action="document_analysis",
            payload={"filenames": [f.filename for f in files]},
            result={
                "comparison_id": saved_comparison.id,
                "decision_summary": goals["best_options"],
            },
        )

        return {
            "documents": [
                {
                    "id": d.id,
                    "filename": d.filename,
                    "preview": d.preview,
                    "summary": s.summary,
                }
                for d, s in zip(saved_docs, saved_summaries)
            ],
            "comparison": {
                "table": table["comparison_table"],
                "decision_summary": goals["best_options"],
            },
        }
