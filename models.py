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
   
    # 보드란 칼럼 - Board클래스를 참조, writer와 백 팝
    boards = relationship("Board", back_populates="writer") 


class Board(Base):
    __tablename__  = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    writer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(timezone('Asia/Seoul')))
   
    # (보낸다) 커맨츠라는 칼럼 -Commnet 클래스를 참조, board와 백팝
    comments = relationship("Comment", back_populates="board")
    # (받는다) User를 참조, User 클래스 안의 boards와 백팝
    writer = relationship("User", back_populates="boards")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    context = Column(String, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"))
    created_at = Column(DateTime, default=datetime.now(timezone('Asia/Seoul')))
    
    # (받는다) Board 클래스 참조,  Board클래스 안의 Comments와 백팝
    board = relationship("Board", back_populates="comments")
