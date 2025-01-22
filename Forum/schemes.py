from pydantic import BaseModel
from pydantic import Field

class Base(BaseModel):
    ...

class UserSchema(Base):
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=8)

class CommentSchema(Base):
    comment: str

class ThreadSchema(Base):
    thread_title: str
    thread_text: str = Field(min_length=10)