from typing import List, Optional

from datetime import datetime
from pydantic import BaseModel


class BoardBase(BaseModel):
    title: str
    content: Optional[str] = None
    

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    created_at: datetime
    writer_id: int
    
    class Config:
        orm_mode = True


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
