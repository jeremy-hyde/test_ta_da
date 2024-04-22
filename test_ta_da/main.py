from datetime import datetime

from fastapi import FastAPI, Request
from .api import articles_router
from .models import articles
from .core.database import engine

app = FastAPI()


@app.middleware("http")
async def log_request(request: Request, call_next):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{now}: {request.method} {request.url}")
    response = await call_next(request)
    return response


app.include_router(articles_router.router)

articles.Base.metadata.create_all(bind=engine)
