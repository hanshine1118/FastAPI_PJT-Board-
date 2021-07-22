from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false, true


from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "users",
        "description" : "users CRUD"
    },{
        "name": "boards",
        "description" : "boards CRUD"
    }
]

app = FastAPI(
    title="user board app",
    description= "user and board are available to CRUD",
    openapi_tags = tags_metadata
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def isBoardExist(db, board_id):
    # id값으로 해당 board가 있는지 검사
    db_board = crud.get_board(db, board_id)
    if not db_board:
        return False
    return True

# user CRUD

@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=403, detail="Email has been used")

    return crud.create_user(db=db, user=user)

@app.get('/users/', response_model=List[schemas.User], tags=["users"])
def read_users(db: Session=Depends(get_db)):
    users = crud.get_users(db=db)
    return users

@app.delete('/users/delete/{user_id}', response_model=schemas.User, tags=["users"])
def delete_user(user_id: int, db : Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(403, detail="There's no user with the id")
    user = crud.delete_user(db, user_id)
    return user

@app.put('/users/update/{user_id}', response_model=schemas.User, tags=["users"])
def update_user(user_id: int, user: schemas.UserBase, db : Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=403, detail="There no such user with ID")
    user = crud.update_user(db, db_user.id, user.email)
    
    return user


# board CRUD

@app.post('/user/{user_id}/boards/', response_model=schemas.Board, tags=["boards"])
def create_board(user_id: int, board:schemas.BoardCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=403, detail="There's no user with the id#")
    return crud.create_board(db=db, board=board, writer_id=user_id)

@app.get('/boards/{board_id}', response_model=schemas.Board, tags=["boards"])
def read_board(board_id: int, db: Session= Depends(get_db)):
    return crud.get_board(db, board_id)

@app.get('/boards/', response_model=List[schemas.Board], tags=["boards"])
def read_boards(db: Session=Depends(get_db)):
    users= crud.get_boards(db)
    return users

@app.delete('/delete/{board_id}', response_model=schemas.Board, tags=["boards"])
def delete_board(board_id: int, db: Session= Depends(get_db)):
    if isBoardExist(db, board_id) == False:
        raise HTTPException(status_code=403, detail="There's no board")
    return crud.delete_board(db, board_id)

@app.put('/boards/update/{board_id}', response_model=schemas.Board, tags=['boards'])
def update_board(board_id: int, board: schemas.BoardCreate, db: Session= Depends(get_db)):
    if isBoardExist(db, board_id) == False:
        raise HTTPException(status_code=403, detail="There's no board")
    return crud.update_baord(db, board_id, board.title, board.content)

@app.get('/users/{user_id}/boards/', response_model=List[schemas.Board], tags=['boards'])
def read_boards_by_writer_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_boards_by_writer_id(db, writer_id=user_id)
    