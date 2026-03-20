from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime

    # the below is for letting pydantic to convert the sqlalchemy model to dictionary
    class Config:
        from_attributes = True