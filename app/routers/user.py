from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from app import models
from app.database import engine, get_db
from app.schemas import UserBase, UserOut, UUser, User
from typing import List
from app.utils import hash_password
from app.oauth2 import get_current_user

router = APIRouter(tags=["Users"])


@router.get("/")
def home():
    return "hello world!"


@router.post("/user", response_model=UserOut)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    hashed_password = hash_password(request.password)
    request.password = hashed_password
    new_user = models.Users(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/all", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@router.get("/user/{id}", response_model=User)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exists",
        )
    return user


@router.put(
    "/user/{id}",
    response_model=User,
)
def update_user(
    id: int,
    request: UUser,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exists",
        )
    user_query.update(request.dict(), synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/user/delete/{id}")
def delete_user(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exists",
        )
    user_query.delete()
    db.commit()
    return {"message": "deleted Successfully"}
