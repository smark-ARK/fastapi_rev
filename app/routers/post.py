from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from app.models import Posts
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import PostBase, PostOut, PostUpdate
import shutil
import multipart, aiofiles


router = APIRouter(prefix="/post", tags=["Posts"])


@router.post("/", response_model=PostOut)
def create_post(
    request: PostBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_post = Posts(user_id=current_user.id, **request.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/all", response_model=List[PostOut])
def get_all(db: Session = Depends(get_db)):
    posts = db.query(Posts).all()
    return posts


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == id).first()
    return post


@router.put("/{id}", response_model=PostOut)
def get_post(
    request: PostUpdate,
    id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post_query = db.query(Posts).filter(Posts.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} not found!!",
        )
    post_query.update(request.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/delete/{id}")
def delete_post(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    post_query = db.query(Posts).filter(Posts.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} not found!!",
        )
    post_query.delete()
    db.commit()
    return {"message": "Deleted Successfully"}


@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user=Depends(get_current_user)):
    filename = image.filename
    path = f"static/{filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        buffer.close()

    return {"path": path}
