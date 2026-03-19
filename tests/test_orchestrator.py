import pytest
from io import BytesIO
from types import SimpleNamespace
from fastapi import HTTPException, UploadFile

from app.services.comparison_orchestrator import DocumentOrchestrator


class FakeSummary:
    def model_dump(self):
        return {
            "document_type": "Contract",
            "main_purpose": "Test purpose",
            "key_points": ["A"],
            "pros": ["P"],
            "cons": ["C"],
            "risk_flags": ["R"],
        }


class FakeDocumentService:
    async def process_single(self, file):
        return {
            "filename": file.filename,
            "preview": f"preview-{file.filename}",
            "text": f"text-{file.filename}",
        }

    async def save_document(self, db, user_id, file, preview, text):
        return SimpleNamespace(
            id=len(db.saved_docs) + 1,
            filename=file.filename,
            preview=preview,
            text=text,
        )

    async def save_summary(self, db, document, summary):
        return SimpleNamespace(document_id=document.id, summary=summary)


class FakeSummaryService:
    async def generate(self, text):
        return FakeSummary()


class FakeComparisonService:
    def comparison_table(self, files_data):
        return {"comparison_table": [{"criterion": "Document type", "values": {}}]}

    async def save_comparison(self, db, user_id, documents, table, decision_summary):
        return SimpleNamespace(id=99)


class FakeDecisionService:
    async def goal_analysis(self, parsed_files, table):
        return {"best_options": [{"winner": parsed_files[0]["filename"]}]}


class FakeHistoryService:
    async def add(self, db, user_id, action, payload, result):
        return SimpleNamespace(id=1)


class FakeDB:
    def __init__(self):
        self.committed = False
        self.rolled_back = False
        self.saved_docs = []

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True


@pytest.fixture
def orchestrator():
    return DocumentOrchestrator(
        document_service=FakeDocumentService(),
        comparison_service=FakeComparisonService(),
        decision_service=FakeDecisionService(),
        history_service=FakeHistoryService(),
        summary_service=FakeSummaryService(),
    )


def make_upload_file(name: str):
    return UploadFile(filename=name, file=BytesIO(b"hello"))


@pytest.mark.asyncio
async def test_returns_anonymous_response(orchestrator):
    db = FakeDB()
    files = [make_upload_file("a.txt"), make_upload_file("b.txt")]

    result = await orchestrator.process_documents(files=files, user=None, db=db)

    assert len(result["documents"]) == 2
    assert "id" not in result["documents"][0]
    assert result["comparison"]["decision_summary"][0]["winner"] == "a.txt"
    assert db.committed is False


@pytest.mark.asyncio
async def test_raises_for_invalid_count(orchestrator):
    db = FakeDB()
    files = [make_upload_file("only_one.txt")]

    with pytest.raises(HTTPException) as exc:
        await orchestrator.process_documents(files=files, user=None, db=db)

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_commits_for_authenticated_user(orchestrator):
    db = FakeDB()
    user = SimpleNamespace(id=10)
    files = [make_upload_file("a.txt"), make_upload_file("b.txt")]

    result = await orchestrator.process_documents(files=files, user=user, db=db)

    assert db.committed is True
    assert len(result["documents"]) == 2
    assert result["documents"][0]["id"] == 1


@pytest.mark.asyncio
async def test_rolls_back_on_failure():
    class FailingDocumentService(FakeDocumentService):
        async def save_summary(self, db, document, summary):
            raise RuntimeError("db error")

    orchestrator = DocumentOrchestrator(
        document_service=FailingDocumentService(),
        comparison_service=FakeComparisonService(),
        decision_service=FakeDecisionService(),
        history_service=FakeHistoryService(),
        summary_service=FakeSummaryService(),
    )

    db = FakeDB()
    user = SimpleNamespace(id=10)
    files = [make_upload_file("a.txt"), make_upload_file("b.txt")]

    with pytest.raises(RuntimeError):
        await orchestrator.process_documents(files=files, user=user, db=db)

    assert db.rolled_back is True
