from sqlalchemy.orm import Session

from ..models.articles import Article
from ..schemas.articles import ArticleCreate


class ArticleRepository:
    def create_article(self, db: Session, obj_in: ArticleCreate) -> None:
        db_obj = Article(title=obj_in.title, author=obj_in.author, content=obj_in.content)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def get_by_id(self, db: Session, article_id: int) -> Article | None:
        return db.query(Article).filter(Article.id == article_id).first()

    def get_all(self, db: Session) -> list[Article]:
        return db.query(Article).all()

    def delete(self, db: Session, article: Article) -> None:
        db.delete(article)
        db.commit()


article_repository = ArticleRepository()
