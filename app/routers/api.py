# coding: utf-8

import os
from mongoengine import connect
from fastapi import APIRouter
from app.database.models import Article
from app.database.utils import mongo_to_dict
router = APIRouter(prefix="/api", tags=["Api"])


@router.get("/articles")
def articles(skip: int = 0, limit: int = 10):
    connect(host=os.environ["MONGODB_URL"])
    count = Article.objects.count()
    if skip + limit > count:
        return {"error": "Database counts only {count} articles."}, 400
    elif skip < 0:
        return {"error": "`skip` argument must be >= 0."}, 400
    elif skip > limit:
        return {
            "error": (
                "`skip` argument value cannot be higher than `limit`"
                " argument value."
            )
        }, 400

    articles = [
        mongo_to_dict(article) for article in Article.objects[skip:skip + limit]
    ]
    return {"count": len(articles), "items": articles}