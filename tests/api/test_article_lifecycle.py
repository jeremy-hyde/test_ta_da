from starlette.testclient import TestClient

from test_ta_da.schemas.articles import ArticleCreate


#
# Make sure the complete lifecycle works
#


def test_article_lifecycle(client: TestClient):
    # Create an article
    article_1 = ArticleCreate(title="Article 1", author="Author 1", content="Content 1")
    r = client.post("/articles/", json=article_1.model_dump())
    assert r.status_code == 200
    assert r.json() == {"detail": "ok"}

    # Create another article
    article_2 = ArticleCreate(title="Article 2", author="Author 2", content="Content 2")
    r = client.post("/articles/", json=article_2.model_dump())
    assert r.status_code == 200
    assert r.json() == {"detail": "ok"}

    # List the 2 articles
    r = client.get("/articles/")
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 2
    assert content[0]["title"] == article_1.title
    assert content[1]["title"] == article_2.title

    # Delete the first one
    r = client.delete("/articles/1/")
    assert r.status_code == 200
    assert r.json() == {"detail": "ok"}

    # List the only article left
    r = client.get("/articles/")
    assert r.status_code == 200
    content = r.json()
    assert len(content) == 1
    assert content[0]["title"] == article_2.title
