#this is : schemas.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# =================================USER SCHEMAS=============================
class UserBase(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)




#request
class UserCreate(UserBase):
   pass



#response form
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    pass
# =================================POST SCHEMAS=============================

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    model_config = ConfigDict(from_attributes=True)


# schema for the request that the server gets
class PostCreate(PostBase):
    pass


# schema for the response that the server sends
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner : UserOut
    model_config = ConfigDict(from_attributes=True)


# =================================TOKEN SCHEMAS=============================

class Token(BaseModel):
    access_token: str
    token_type: str
    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    email: Optional[str] = None
    exp: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)




