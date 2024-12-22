#this is : main.py
from fastapi import FastAPI
from app.db.database import Base,engine
from app.routers import post, auth, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Worldaaaaddddsdsadaa"}



