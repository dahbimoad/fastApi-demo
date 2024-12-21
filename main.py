from http.client import responses

from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from starlette import status
from database import Base,engine,get_db
import schemas
import models
from utils import hash_password

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
    db.refresh(new_post)
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



#=========================USER==========================================
@app.post("/users" ,response_model=schemas.UserOut , status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate ,db:Session = Depends(get_db)):
       # hash the password
        user.password = hash_password(user.password)

        new_user = models.User(**user.dict())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@app.get("/user/{id}",response_model=schemas.UserOut,status_code=status.HTTP_200_OK)
def get_user(id : int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
            raise HTTPException(status_code=404, detail="User not found")
    return user