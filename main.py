from fastapi import FastAPI, Body
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import models




Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello Worldaaaaa"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/posts/create")
def create_post(request_data : dict = Body(...)):
    return {"post data:": f"title: {request_data['title']} + content: {request_data['content']}"}

