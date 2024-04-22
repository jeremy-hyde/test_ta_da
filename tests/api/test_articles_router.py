from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from test_ta_da.schemas.articles import ArticleCreate
from tests.conftest import create_article_in_db


#
# create_article
#


def test_create_article_200(client: TestClient, article: ArticleCreate):
    r = client.post("/articles/", json=article.model_dump())
    assert r.status_code == 200
    assert r.json() == {"detail": "ok"}


def test_create_article_422_invalid_title(client: TestClient, article: ArticleCreate):
    article.title = None
    r = client.post("/articles/", json=article.model_dump())
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"][1] == "title"
    assert r.json()["detail"][0]["msg"] == "Input should be a valid string"


def test_create_article_422_invalid_author(client: TestClient, article: ArticleCreate):
    article.author = None
    r = client.post("/articles/", json=article.model_dump())
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"][1] == "author"
    assert r.json()["detail"][0]["msg"] == "Input should be a valid string"


def test_create_article_422_invalid_content(client: TestClient, article: ArticleCreate):
    article.content = None
    r = client.post("/articles/", json=article.model_dump())
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"][1] == "content"
    assert r.json()["detail"][0]["msg"] == "Input should be a valid string"


#
# get_articles
#


def test_get_articles_200_empty(client: TestClient):
    r = client.get("/articles/")
    assert r.status_code == 200
    assert r.json() == []


def test_get_articles_200_multiples_results(client: TestClient, session: Session):
    # Create 2 articles in db
    article_1 = create_article_in_db(session, "1")
    article_2 = create_article_in_db(session, "2")

    r = client.get("/articles/")
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 2
    assert content[0]["id"]
    assert content[0]["title"] == article_1.title
    assert content[0]["author"] == article_1.author
    assert content[0]["created_at"]
    assert content[0]["content"] == article_1.content

    assert content[1]["id"]
    assert content[1]["title"] == article_2.title
    assert content[1]["author"] == article_2.author
    assert content[1]["created_at"]
    assert content[1]["content"] == article_2.content


#
# delete_article
#


def test_delete_article_200(client: TestClient, session: Session):
    # Create article in db
    create_article_in_db(session, "1")
    r = client.delete("/articles/1/")
    assert r.status_code == 200
    assert r.json() == {"detail": "ok"}


def test_delete_article_422_invalid_id(client: TestClient, session: Session):
    r = client.delete("/articles/aa/")
    assert r.status_code == 422
    assert (
        r.json()["detail"][0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )


def test_delete_article_404(client: TestClient, session: Session):
    r = client.delete("/articles/1/")
    assert r.status_code == 404
    assert r.json() == {"detail": "Article not found"}
