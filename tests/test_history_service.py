import pytest

from app.services.history_service import HistoryService
from tests.factories import (
    UserFactory,
    DocumentFactory,
    DocumentSummaryFactory,
    ComparisonFactory,
    UserHistoryFactory,
)


class FakeComparisonService:
    def __init__(self, comparison, documents):
        self._comparison = comparison
        self._documents = documents

    async def get_by_id(self, db, comparison_id):
        return self._comparison

    async def get_documents_for_comparison(self, db, comparison_id):
        return self._documents


class FakeDocumentService:
    def __init__(self, summaries_map):
        self._summaries_map = summaries_map

    async def get_summaries_for_documents(self, db, doc_ids):
        return self._summaries_map


@pytest.mark.asyncio
async def test_get_history_documents_and_comparison(db_session):
    user = UserFactory.build()

    doc1 = DocumentFactory.build(
        user=user, user_id=user.id, filename="a.txt", preview="A preview"
    )
    doc2 = DocumentFactory.build(
        user=user, user_id=user.id, filename="b.txt", preview="B preview"
    )

    comparison = ComparisonFactory.build(user=user, user_id=user.id)

    history = UserHistoryFactory.build(
        user=user,
        user_id=user.id,
        result={
            "comparison_id": comparison.id,
            "decision_summary": comparison.decision_summary,
        },
    )

    summary1 = DocumentSummaryFactory.build(document=doc1, document_id=doc1.id)
    summary2 = DocumentSummaryFactory.build(document=doc2, document_id=doc2.id)

    db_session.add_all([user, doc1, doc2, comparison, history, summary1, summary2])
    await db_session.flush()

    service = HistoryService(
        history_model=type(history),
        comparison_service=FakeComparisonService(comparison, [doc1, doc2]),
        document_service=FakeDocumentService(
            {
                doc1.id: summary1.summary,
                doc2.id: summary2.summary,
            }
        ),
    )

    result = await service.get_history_item(
        db=db_session,
        history_id=history.id,
        user_id=user.id,
    )

    assert len(result["documents"]) == 2
    assert result["comparison"]["decision_summary"] == comparison.decision_summary
