from datetime import datetime

from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# schema for the request that the server gets
class PostCreate(PostBase):
    pass

#class PostUpdate(PostBase):

#class PostDelete(PostBase):


# schema for the response that the server sends
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes  = True