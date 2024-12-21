from fastapi import FastAPI, Body

from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello Worldaaaaa"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/posts/create")
def create_post(request_data : dict = Body(...)):
    return {"post data:": f"title: {request_data['title']} + content: {request_data['content']}"}

