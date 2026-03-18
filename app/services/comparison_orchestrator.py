from fastapi import HTTPException, UploadFile


class DocumentOrchestrator:
    def __init__(
        self,
        document_service,
        comparison_service,
        decision_service,
        history_service,
        summary_service,
    ):
        self.document_service = document_service
        self.comparison_service = comparison_service
        self.decision_service = decision_service
        self.history_service = history_service
        self.summary_service = summary_service

    async def process_documents(self, files: list[UploadFile], user, db) -> dict:
        self._validate_files_count(files)

        analyzed_docs = await self._analyze_documents(files)
        comparison = await self._build_comparison(analyzed_docs)

        if not user:
            return self._build_anonymous_response(analyzed_docs, comparison)

        return await self._persist_and_build_response(
            db=db,
            user=user,
            files=files,
            analyzed_docs=analyzed_docs,
            comparison=comparison,
        )

    def _validate_files_count(self, files: list[UploadFile]) -> None:
        if not 2 <= len(files) <= 5:
            raise HTTPException(
                status_code=400,
                detail="You must upload from 2 to 5 documents.",
            )

    async def _analyze_documents(self, files: list[UploadFile]) -> list[dict]:
        analyzed_docs = []

        for file in files:
            parsed = await self.document_service.process_single(file)
            summary = await self.summary_service.generate(parsed["text"])
            parsed["summary"] = summary.model_dump()
            analyzed_docs.append(parsed)

        return analyzed_docs

    async def _build_comparison(self, analyzed_docs: list[dict]) -> dict:
        table = self.comparison_service.comparison_table(analyzed_docs)
        goals = await self.decision_service.goal_analysis(analyzed_docs, table)

        return {
            "table": table["comparison_table"],
            "decision_summary": goals["best_options"],
        }

    def _build_anonymous_response(
        self, analyzed_docs: list[dict], comparison: dict
    ) -> dict:
        return {
            "documents": [
                {
                    "filename": d["filename"],
                    "preview": d["preview"],
                    "summary": d["summary"],
                }
                for d in analyzed_docs
            ],
            "comparison": comparison,
        }

    async def _persist_and_build_response(
        self,
        db,
        user,
        files: list[UploadFile],
        analyzed_docs: list[dict],
        comparison: dict,
    ) -> dict:
        try:
            saved_docs = await self._save_documents(
                db=db,
                user_id=user.id,
                files=files,
                analyzed_docs=analyzed_docs,
            )

            saved_summaries = await self._save_summaries(
                db=db,
                saved_docs=saved_docs,
                analyzed_docs=analyzed_docs,
            )

            saved_comparison = await self.comparison_service.save_comparison(
                db=db,
                user_id=user.id,
                documents=saved_docs,
                table={"comparison_table": comparison["table"]},
                decision_summary=comparison["decision_summary"],
            )

            await self.history_service.add(
                db=db,
                user_id=user.id,
                action="document_analysis",
                payload={"filenames": [f.filename for f in files]},
                result={
                    "comparison_id": saved_comparison.id,
                    "decision_summary": comparison["decision_summary"],
                },
            )

            await db.commit()

        except Exception:
            await db.rollback()
            raise

        return self._build_persisted_response(
            saved_docs=saved_docs,
            saved_summaries=saved_summaries,
            comparison=comparison,
        )

    async def _save_documents(
        self, db, user_id: int, files: list[UploadFile], analyzed_docs: list[dict]
    ):
        saved_docs = []

        for file, parsed in zip(files, analyzed_docs):
            doc = await self.document_service.save_document(
                db=db,
                user_id=user_id,
                file=file,
                preview=parsed["preview"],
                text=parsed["text"],
            )
            saved_docs.append(doc)

        return saved_docs

    async def _save_summaries(self, db, saved_docs: list, analyzed_docs: list[dict]):
        saved_summaries = []

        for doc, parsed in zip(saved_docs, analyzed_docs):
            summary_obj = await self.document_service.save_summary(
                db=db,
                document=doc,
                summary=parsed["summary"],
            )
            saved_summaries.append(summary_obj)

        return saved_summaries

    def _build_persisted_response(
        self, saved_docs: list, saved_summaries: list, comparison: dict
    ) -> dict:
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
            "comparison": comparison,
        }


# class DocumentOrchestrator:
#     def __init__(
#         self,
#         document_service,
#         comparison_service,
#         decision_service,
#         history_service,
#         summary_service,
#     ):
#         self.document_service = document_service
#         self.comparison_service = comparison_service
#         self.decision_service = decision_service
#         self.history_service = history_service
#         self.summary_service = summary_service

#     def _parse_llm_json(self, raw: str, context: str) -> dict:
#         if not raw or not raw.strip():
#             raise HTTPException(
#                 status_code=502,
#                 detail=f"LLM returned empty response for {context}",
#             )

#         try:
#             return json.loads(raw)
#         except json.JSONDecodeError:
#             raise HTTPException(
#                 status_code=502,
#                 detail=f"LLM returned invalid JSON for {context}",
#             )

#     async def process_documents(self, files: list[UploadFile], user, db) -> dict:
#         if not 2 <= len(files) <= 5:
#             raise HTTPException(
#                 status_code=400,
#                 detail="You must upload from 2 to 5 documents.",
#             )

#         parsed_files = []
#         for file in files:
#             parsed = await self.document_service.process_single(file)
#             summary = await self.summary_service.generate(parsed["text"])
#             parsed["summary"] = summary.model_dump()
#             parsed_files.append(parsed)

#         table = self.comparison_service.comparison_table(parsed_files)
#         goals = await self.decision_service.goal_analysis(parsed_files, table)

#         if not user:
#             return {
#                 "documents": [
#                     {
#                         "filename": d["filename"],
#                         "preview": d["preview"],
#                         "summary": d["summary"],
#                     }
#                     for d in parsed_files
#                 ],
#                 "comparison": {
#                     "table": table["comparison_table"],
#                     "decision_summary": goals["best_options"],
#                 },
#             }

#         try:
#             saved_docs = []
#             for f, parsed in zip(files, parsed_files):
#                 doc = await self.document_service.save_document(
#                     db=db,
#                     user_id=user.id,
#                     file=f,
#                     preview=parsed["preview"],
#                     text=parsed["text"],
#                 )
#                 saved_docs.append(doc)

#             saved_summaries = []
#             for doc, parsed in zip(saved_docs, parsed_files):
#                 summary_obj = await self.document_service.save_summary(
#                     db=db,
#                     document=doc,
#                     summary=parsed["summary"],
#                 )
#                 saved_summaries.append(summary_obj)

#             saved_comparison = await self.comparison_service.save_comparison(
#                 db=db,
#                 user_id=user.id,
#                 documents=saved_docs,
#                 table=table,
#                 decision_summary=goals["best_options"],
#             )

#             await self.history_service.add(
#                 db=db,
#                 user_id=user.id,
#                 action="document_analysis",
#                 payload={"filenames": [f.filename for f in files]},
#                 result={
#                     "comparison_id": saved_comparison.id,
#                     "decision_summary": goals["best_options"],
#                 },
#             )

#             await db.commit()

#         except Exception:
#             await db.rollback()
#             raise

#         return {
#             "documents": [
#                 {
#                     "id": d.id,
#                     "filename": d.filename,
#                     "preview": d.preview,
#                     "summary": s.summary,
#                 }
#                 for d, s in zip(saved_docs, saved_summaries)
#             ],
#             "comparison": {
#                 "table": table["comparison_table"],
#                 "decision_summary": goals["best_options"],
#             },
#         }
