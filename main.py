#this is : main.py
from fastapi import FastAPI
from jose import jwt

from app.core.config import settings
from app.db.database import Base,engine
from app.routers import post, auth, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    decoded = jwt.decode(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1vdWFkZGFoYmlAZ21haWwuY29tIiwiZXhwIjoxNzM0OTE2NTQ3fQ.eQRelIpddLKhI6kVGNjgqWjXnV4gzJa0BS0HZp18FOE",
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    print(decoded)
    return {"message": "Hello World"}



