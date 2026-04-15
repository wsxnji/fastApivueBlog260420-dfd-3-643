from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=schemas.Token)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=user_login.username)
    if not user or user.password != user_login.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {
        "access_token": user.username,
        "token_type": "bearer",
        "user": user
    }


@router.get("/users", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
