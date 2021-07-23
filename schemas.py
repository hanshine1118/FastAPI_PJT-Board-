from my_app.database import Base
from typing import List, Optional

from datetime import datetime
from pydantic import BaseModel

# Comments

class CommentBase(BaseModel):
    context: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime
    board_id: int
    
    class Config:
        orm_mode = True


# 게시글

class BoardBase(BaseModel):
    title: str
    content: Optional[str] = None
    

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    created_at: datetime
    writer_id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True

# 유저
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    

class User(UserBase):
    id: int
    boards: List[Board] = []
    created_at: datetime
    class Config:
        orm_mode= True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None



