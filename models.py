from enum import auto
from re import L
from sqlalchemy import ForeignKey, Integer, String, Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKeyConstraint

from datetime import datetime
from pytz import timezone

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone('Asia/Seoul')))

    boards = relationship("Board", back_populates="writer")

class Board(Base):
    __tablename__  = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    writer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(timezone('Asia/Seoul')))

    writer = relationship("User", back_populates="boards")
