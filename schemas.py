from datetime import datetime

from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# schema for the request that the server gets
class PostCreate(PostBase):
    pass


# schema for the response that the server sends
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes  = True

#================================USER=============================
class UserBase(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int



class UserCreate(UserBase):
   pass