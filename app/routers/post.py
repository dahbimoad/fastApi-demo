#this is : routes/post.py
from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from app import schemas, models, oauth2
from app.db.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts :)"],
)

# Endpoint: Create a new post
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(
    oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Endpoint: Get all posts
@router.get("/", response_model=list[schemas.Post], status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user), search :Optional[str] = ""):
    return db.query(models.Post).filter(models.Post.title.contains(search)).all()

# Endpoint: Get a specific post by ID
@router.get("/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post

# Endpoint: Update an existing post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: schemas.UserOut = Depends(
    oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this post")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()



# Endpoint: Delete a specific post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(
    oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Post deleted successfully"}

