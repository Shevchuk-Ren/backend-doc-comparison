from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, Text
from app.db.base import Base
from sqlalchemy.orm import relationship


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    file_type = Column(String)
    size = Column(Integer)
    text = Column(Text)
    preview = Column(Text)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="documents")
    summaries = relationship(
        "DocumentSummary", back_populates="document", cascade="all, delete-orphan"
    )
    comparisons = relationship(
        "Comparison", secondary="comparison_documents", back_populates="documents"
    )
