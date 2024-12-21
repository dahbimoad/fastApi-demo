
from fastapi import FastAPI
from database import Base,engine
from routers import user, post

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Hello Worldaaaaa"}



