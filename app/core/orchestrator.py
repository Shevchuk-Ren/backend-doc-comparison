from app.services.document_parser import DocumentParser
from app.services.ollama_service import OllamaService
from app.services.comparison_service import ComparisonService
from app.services.decision_service import DecisionService
from app.services.document_service import DocumentService
from app.services.comparison_orchestrator import DocumentOrchestrator
from app.validators.document_validator import DocumentValidator

validator = DocumentValidator()
parser = DocumentParser()

document_service = DocumentService(validator, parser)
ollama_service = OllamaService()
comparison_service = ComparisonService()
decision_service = DecisionService()

orchestrator = DocumentOrchestrator(
    document_service, ollama_service, comparison_service, decision_service
)
