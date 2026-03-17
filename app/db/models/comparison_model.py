from sqlalchemy import Column, DateTime, Integer, func, ForeignKey, JSON
from app.db.base import Base
from sqlalchemy.orm import relationship


class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comparison_table = Column(JSON)
    decision_summary = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())


class ComparisonDocument(Base):
    __tablename__ = "comparison_documents"

    comparison_id = Column(Integer, ForeignKey("comparisons.id"), primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), primary_key=True)

    user = relationship("User", back_populates="comparisons")
    documents = relationship(
        "DocumentModel", secondary="comparison_documents", back_populates="comparisons"
    )
