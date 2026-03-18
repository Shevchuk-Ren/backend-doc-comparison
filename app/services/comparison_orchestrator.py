from fastapi import HTTPException, UploadFile
import json


class DocumentOrchestrator:
    def __init__(
        self,
        document_service,
        llm,
        comparison_service,
        decision_service,
        history_service,
        summary_service,
    ):
        self.document_service = document_service
        self.llm = llm
        self.comparison_service = comparison_service
        self.decision_service = decision_service
        self.history_service = history_service
        self.summary_service = summary_service

    def _parse_llm_json(self, raw: str, context: str) -> dict:
        if not raw or not raw.strip():
            raise HTTPException(
                status_code=502,
                detail=f"LLM returned empty response for {context}",
            )

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=502,
                detail=f"LLM returned invalid JSON for {context}",
            )

    async def process_documents(self, files: list[UploadFile], user, db) -> dict:
        if not 2 <= len(files) <= 5:
            raise HTTPException(
                status_code=400,
                detail="You must upload from 2 to 5 documents.",
            )

        parsed_files = []
        for file in files:
            parsed = await self.document_service.process_single(file)
            # summary_raw = await self.llm.chat(
            #     system_prompt=SYSTEM_PROMPT,
            #     user_prompt=build_document_prompt(parsed["text"]),
            # )
            summary = await self.summary_service.generate(parsed["text"])
            parsed["summary"] = summary.model_dump()
            # parsed["summary"] = self._parse_llm_json(
            #     summary_raw, context="document summary"
            # )
            # parsed["summary"] = json.loads(summary_raw)
            parsed_files.append(parsed)

        table = self.comparison_service.comparison_table(parsed_files)
        goals = await self.decision_service.goal_analysis(parsed_files, table)
        print(user)
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

        try:
            saved_docs = []
            for f, parsed in zip(files, parsed_files):
                doc = await self.document_service.save_document(
                    db=db,
                    user_id=user.id,
                    file=f,
                    preview=parsed["preview"],
                    text=parsed["text"],
                )
                saved_docs.append(doc)

            saved_summaries = []
            for doc, parsed in zip(saved_docs, parsed_files):
                summary_obj = await self.document_service.save_summary(
                    db=db,
                    document=doc,
                    summary=parsed["summary"],
                )
                saved_summaries.append(summary_obj)

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

            await db.commit()

        except Exception:
            await db.rollback()
            raise

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
