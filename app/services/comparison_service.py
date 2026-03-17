from app.db.models.document_model import DocumentModel
from sqlalchemy import select


class ComparisonService:
    def __init__(self, ComparisonModel, ComparisonDocumentModel):
        self.ComparisonModel = ComparisonModel
        self.ComparisonDocumentModel = ComparisonDocumentModel
        self.DocumentModel = DocumentModel

    def comparison_table(self, files_data):
        table = [
            {
                "criterion": "Document type",
                "values": {
                    doc["filename"]: doc["summary"].get("document_type")
                    for doc in files_data
                },
            },
            {
                "criterion": "Main purpose",
                "values": {
                    doc["filename"]: doc["summary"].get("main_purpose")
                    for doc in files_data
                },
            },
            {
                "criterion": "Key points",
                "values": {
                    doc["filename"]: doc["summary"].get("key_points", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Pros",
                "values": {
                    doc["filename"]: doc["summary"].get("pros", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Cons",
                "values": {
                    doc["filename"]: doc["summary"].get("cons", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Risk flags",
                "values": {
                    doc["filename"]: doc["summary"].get("risk_flags", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Decision summary",
                "values": {
                    doc["filename"]: doc["summary"].get("decision_summary")
                    for doc in files_data
                },
            },
        ]

        return {"comparison_table": table}

    async def save_comparison(self, db, user_id, documents, table, decision_summary):
        comp = self.ComparisonModel(
            user_id=user_id,
            comparison_table=table["comparison_table"],
            decision_summary=decision_summary,
        )
        db.add(comp)
        await db.commit()
        await db.refresh(comp)

        # зв’язуємо comparison ↔ documents
        for doc in documents:
            link = self.ComparisonDocumentModel(
                comparison_id=comp.id, document_id=doc.id
            )
            db.add(link)

        await db.commit()
        return comp

    async def get_by_id(self, db, comparison_id):
        return await db.get(self.ComparisonModel, comparison_id)

    async def get_documents_for_comparison(self, db, comparison_id):
        q = await db.execute(
            select(self.ComparisonDocumentModel).where(
                self.ComparisonDocumentModel.comparison_id == comparison_id
            )
        )
        links = q.scalars().all()
        doc_ids = [link.document_id for link in links]
        if not doc_ids:
            return []

        q2 = await db.execute(
            select(self.DocumentModel).where(self.DocumentModel.id.in_(doc_ids))
        )
        return q2.scalars().all()
