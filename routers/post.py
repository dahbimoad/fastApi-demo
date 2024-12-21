
from fastapi import FastAPI, Body, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
import schemas
import models


router = APIRouter(
    prefix="/posts",
    tags=["Posts :)"],
)


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[schemas.Post], status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@router.get("/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{id}", response_model=schemas.Post,)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Post deleted successfully"}

