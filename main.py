from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import schemas
from database import Base,engine,get_db
import models




Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Worldaaaaa"}

@app.post("/posts/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Refresh to get the newly generated `id` and `created_at`
    return new_post


@app.get("/posts/", response_model=list[schemas.Post], status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@app.get("/posts/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{id}", response_model=schemas.Post,)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Post deleted successfully"}
