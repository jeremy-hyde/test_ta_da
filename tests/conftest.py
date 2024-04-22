from random import random

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from test_ta_da.core.database import Base
from test_ta_da.core.dependencies import get_db
from test_ta_da.main import app
from test_ta_da.repositories.articles import article_repository
from test_ta_da.schemas.articles import ArticleCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # Dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


#
# Articles
#


@pytest.fixture
def get_random_number():
    return str(random() * 10)


@pytest.fixture
def article(get_random_number):
    article = ArticleCreate(
        title="Title test " + get_random_number,
        author="Author test " + get_random_number,
        content="Content Test " + get_random_number,
    )

    return article


def create_article_in_db(session: Session, number: str):
    article = ArticleCreate(
        title="Title test " + number,
        author="Author test " + number,
        content="Content Test " + number,
    )
    article_repository.create_article(session, article)
    return article
