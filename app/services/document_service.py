from fastapi import HTTPException, UploadFile
from sqlalchemy import select


class DocumentService:
    def __init__(self, validator, parser, DocumentModel, SummaryModel):
        self.validator = validator
        self.parser = parser
        self.DocumentModel = DocumentModel
        self.SummaryModel = SummaryModel

    async def process_single(self, file: UploadFile) -> dict:
        validation = await self.validator.validate_file(file)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail={"filename": file.filename, "errors": validation["errors"]},
            )

        parsed = await self.parser.parse(file)
        parsed["size"] = validation["size"]

        return parsed

    async def save_document(self, db, user_id, file, preview, text):
        doc = self.DocumentModel(
            user_id=user_id,
            filename=file.filename,
            preview=preview,
            text=text,
        )
        db.add(doc)
        await db.flush()
        await db.refresh(doc)
        return doc

    async def save_summary(self, db, document, summary):
        summary_obj = self.SummaryModel(
            document_id=document.id,
            summary=summary,
        )
        db.add(summary_obj)
        await db.flush()
        await db.refresh(summary_obj)
        return summary_obj

    async def get_summaries_for_documents(self, db, doc_ids: list[int]):
        q = await db.execute(
            select(self.SummaryModel).where(self.SummaryModel.document_id.in_(doc_ids))
        )
        summaries = q.scalars().all()
        return {s.document_id: s.summary for s in summaries}
