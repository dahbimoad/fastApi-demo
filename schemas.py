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

# =================================USER SCHEMAS=============================
class UserBase(BaseModel):
    email: EmailStr
    password: str



#request
class UserCreate(UserBase):
   pass



#response form
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes  = True


