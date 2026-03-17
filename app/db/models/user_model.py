from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, JSON
from app.db.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    history = relationship(
        "UserHistory", back_populates="user", cascade="all, delete-orphan"
    )
    documents = relationship("DocumentModel", back_populates="user")
    comparisons = relationship("Comparison", back_populates="user")


class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    payload = Column(JSON)
    result = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="history")
