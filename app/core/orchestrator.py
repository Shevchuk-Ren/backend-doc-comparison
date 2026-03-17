from app.services.document_parser import DocumentParser
from app.services.ollama_service import OllamaService
from app.services.comparison_service import ComparisonService
from app.services.history_service import HistoryService
from app.services.decision_service import DecisionService
from app.services.document_service import DocumentService
from app.services.comparison_orchestrator import DocumentOrchestrator
from app.validators.document_validator import DocumentValidator
from app.db.models.document_model import DocumentModel
from app.db.models.summaries_model import DocumentSummary
from app.db.models.user_model import UserHistory
from app.db.models.comparison_model import ComparisonDocument, Comparison

validator = DocumentValidator()
parser = DocumentParser()

document_service = DocumentService(validator, parser, DocumentModel, DocumentSummary)
ollama_service = OllamaService()
comparison_service = ComparisonService(Comparison, ComparisonDocument)
decision_service = DecisionService()
history_service = HistoryService(UserHistory, comparison_service, document_service)

orchestrator = DocumentOrchestrator(
    document_service,
    ollama_service,
    comparison_service,
    decision_service,
    history_service,
)
