# coding: utf-8

import os
from mongoengine import connect
from fastapi import APIRouter
from app.database.documents import Article
from app.database.utils import query_to_dict
router = APIRouter(prefix="/api", tags=["Api"])


@router.get("/articles")
def articles(skip: int = 0, limit: int = 10):
    """List the articles in database. This endpoint provides a `skip` and
    `limit` parameters to navigate among the articles. Throw a 400 HTTP response
    with an error message if arguments are not set properly.

    Args:
        skip (int, optional): how many documents must be skipped. Defaults to 0.
        limit (int, optional): limit to the retrieved number of documents.
            Defaults to 10.
    """
    connect(host=os.environ["MONGODB_URL"])
    count = Article.objects.count()
    if skip + limit > count:
        return {"error": f"Database counts only {count} articles."}, 400
    elif skip < 0:
        return {"error": "`skip` argument must be >= 0."}, 400
    elif skip > limit:
        return {
            "error": (
                "`skip` argument value cannot be higher than `limit`"
                " argument value."
            )
        }, 400

    articles = query_to_dict(query_set=Article.objects[skip:skip + limit])
    return {"count": len(articles), "items": articles}

@router.get("/article")
def article(url: str):
    """Target an article to retrieve with its URL.

    Args:
        url (str): the URL of the article to retrieve.
    """
    connect(host=os.environ["MONGODB_URL"])
    articles = query_to_dict(query_set=Article.objects(url=url))
    return {"article": articles[0]}