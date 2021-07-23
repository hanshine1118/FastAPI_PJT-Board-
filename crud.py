from datetime import datetime, timedelta

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas
from typing import Optional

# 유저 - 가입, 조회, 정보 수정, 삭제
# 게시판 - 게시판 생성,  조회(유저 id로 글 조회, 그냥 글 조회, 전체 글 조회), 수정, 삭제
# pagenation으로 10개씩 게시판 조회
# offset과 skip을 정해서 그값을 올려주면서 보내준다 ㅔpage변수에는 받을 때마다 count+=1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# 유저
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


#회원가입
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    # print(hashed_password)

    db_user = models.User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).offset(0).limit(10).all()

def get_id_by_username(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user.id

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return user

def update_user(db: Session, user_id: int, new_email: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.email = new_email
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 게시판
def create_board(db: Session, board: schemas.BoardCreate, writer_id: int):
    db_board = models.Board(title=board.title, content=board.content, writer_id=writer_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

def get_boards(db: Session):
    return db.query(models.Board).offset(0).limit(20).all()

def get_board(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()

def delete_board(db: Session, board_id: int):
    board = db.query(models.Board).filter(models.Board.id == board_id).first()
    db.delete(board)
    db.commit()
    return board

def update_baord(
    db: Session, 
    board_id: int, 
    new_title: Optional[str]=None, 
    new_content: Optional[str] = None
):
    board = db.query(models.Board).filter(models.Board.id == board_id).first()
    if new_title:
        board.title = new_title
    if new_content:
        board.content = new_content
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

def get_boards_by_writer_id(
    db: Session,
    writer_id: int
):
    boards = db.query(models.Board).filter(models.Board.writer_id == writer_id).all()
    return boards


# 댓글
def create_comment(db: Session, comment: schemas.CommentCreate, board_id: int):
    db_comment = models.Comment(context= comment.context, board_id= board_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    return db_comment

def get_comments(db: Session):
    db_comments = db.query(models.Comment).all()
    return db_comments

def update_comment(db: Session, comment:schemas.Comment, comment_id):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    db_comment.context = comment.context
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    db.delete(db_comment)
    db.commit()

    return db_comment
