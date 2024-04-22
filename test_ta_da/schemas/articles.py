from datetime import datetime

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    author: str
    content: str


class ArticleBase(BaseModel):
    id: int
    title: str
    created_at: datetime
    author: str
    content: str

    class Config:
        from_attributes = True
