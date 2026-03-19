import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.db.models.user_model import User, UserHistory
from app.db.models.document_model import DocumentModel
from app.db.models.summaries_model import DocumentSummary
from app.db.models.comparison_model import Comparison, ComparisonDocument


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    username = factory.Sequence(lambda n: f"user{n}")
    hashed_password = "hashed-password"


class DocumentFactory(BaseFactory):
    class Meta:
        model = DocumentModel

    id = factory.Sequence(lambda n: n + 1)
    user_id = factory.SelfAttribute("user.id")
    user = factory.SubFactory(UserFactory)
    filename = factory.Sequence(lambda n: f"doc_{n}.txt")
    preview = factory.Faker("sentence")
    text = factory.Faker("paragraph")


class DocumentSummaryFactory(BaseFactory):
    class Meta:
        model = DocumentSummary

    id = factory.Sequence(lambda n: n + 1)
    document = factory.SubFactory(DocumentFactory)
    document_id = factory.SelfAttribute("document.id")
    summary = {
        "document_type": "Contract",
        "main_purpose": "Test purpose",
        "key_points": ["A", "B"],
        "pros": ["Pro 1"],
        "cons": ["Con 1"],
        "risk_flags": ["Risk 1"],
    }


class ComparisonFactory(BaseFactory):
    class Meta:
        model = Comparison

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    comparison_table = [
        {
            "criterion": "Document type",
            "values": {"doc_1.txt": "Contract", "doc_2.txt": "Proposal"},
        }
    ]
    decision_summary = {"best_options": [{"winner": "doc_1.txt"}]}


class ComparisonDocumentFactory(BaseFactory):
    class Meta:
        model = ComparisonDocument

    id = factory.Sequence(lambda n: n + 1)
    comparison = factory.SubFactory(ComparisonFactory)
    comparison_id = factory.SelfAttribute("comparison.id")
    document = factory.SubFactory(DocumentFactory)
    document_id = factory.SelfAttribute("document.id")


class UserHistoryFactory(BaseFactory):
    class Meta:
        model = UserHistory

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    action = "document_analysis"
    payload = factory.LazyFunction(lambda: {"filenames": ["doc_1.txt", "doc_2.txt"]})
    result = factory.LazyFunction(
        lambda: {
            "comparison_id": 1,
            "decision_summary": {"best_options": [{"winner": "doc_1.txt"}]},
        }
    )
