from sqlalchemy import Column, Integer, String, DateTime, func

from ..core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    content = Column(String, nullable=False)
