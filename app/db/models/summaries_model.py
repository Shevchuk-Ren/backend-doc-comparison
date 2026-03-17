from sqlalchemy import Column, DateTime, Integer, func, ForeignKey, JSON
from app.db.base import Base
from sqlalchemy.orm import relationship


class DocumentSummary(Base):
    __tablename__ = "document_summaries"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    summary = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    document = relationship("DocumentModel", back_populates="summaries")
