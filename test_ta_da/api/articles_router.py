import sys

from fastapi import APIRouter, Path, HTTPException, Depends
from typing import Annotated

from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..repositories.articles import article_repository
from ..schemas.articles import ArticleBase, ArticleCreate
from ..schemas.message import Message

router = APIRouter()


@router.post("/articles/", response_model=Message)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    article_repository.create_article(db=db, obj_in=article)
    return {"detail": "ok"}


@router.get("/articles/", response_model=list[ArticleBase])
def get_articles(db: Session = Depends(get_db)):
    return article_repository.get_all(db)


@router.delete(
    "/articles/{article_id}/", response_model=Message, responses={404: {"model": Message}}
)
def delete_article(
    article_id: Annotated[int, Path(title="The id of the article to delete", ge=0, lt=sys.maxsize)],
    db: Session = Depends(get_db),
):
    article = article_repository.get_by_id(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    article_repository.delete(db, article)
    return {"detail": "ok"}
