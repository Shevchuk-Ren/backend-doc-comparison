from fastapi import HTTPException
from sqlalchemy import select


class HistoryService:
    def __init__(self, history_model, comparison_service, document_service):
        self.history_model = history_model
        self.comparison_service = comparison_service
        self.document_service = document_service

    async def add(self, db, user_id, action, payload, result):
        record = self.history_model(
            user_id=user_id,
            action=action,
            payload=payload,
            result=result,
        )
        db.add(record)
        await db.flush()
        await db.refresh(record)
        return record

    async def get_history_list(self, db, user_id):
        q = await db.execute(
            select(self.history_model).where(self.history_model.user_id == user_id)
        )
        items = q.scalars().all()

        return [
            {
                "id": h.id,
                "created_at": h.created_at,
                "filenames": h.payload.get("filenames", []),
                "decision_summary": h.result.get("decision_summary"),
                "result_id": h.result.get("comparison_id"),
            }
            for h in items
        ]

    async def get_history_item(self, db, history_id, user_id):
        history = await db.get(self.history_model, history_id)

        if not history or history.user_id != user_id:
            raise HTTPException(status_code=404, detail="History item not found")

        comparison_id = history.result.get("comparison_id")
        if not comparison_id:
            raise HTTPException(status_code=400, detail="Invalid history record")

        # 1. comparison
        comparison = await self.comparison_service.get_by_id(db, comparison_id)

        # 2. documents
        documents = await self.comparison_service.get_documents_for_comparison(
            db, comparison_id
        )

        # 3. summaries
        summaries = await self.document_service.get_summaries_for_documents(
            db, [d.id for d in documents]
        )

        # 4. Формуємо відповідь під HistoryItemOut
        return {
            "documents": [
                {
                    "id": d.id,
                    "filename": d.filename,
                    "preview": d.preview,
                    "summary": summaries[d.id],
                }
                for d in documents
            ],
            "comparison": {
                "table": comparison.comparison_table,
                "decision_summary": comparison.decision_summary,
            },
        }
