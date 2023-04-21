# coding: utf-8

import os

from fastapi import APIRouter

from app.spiders import ArticlesSpider
from app.crawler import Crawler

# from app.db import database, Articles
from app.database.models import Article
# from app.database import client as mongo_client
from mongoengine import connect
from mongoengine.errors import NotUniqueError


router = APIRouter(prefix="/scrapper", tags=["Scrapper"])

@router.post("/retrieve_articles")
async def retrieve_articles():
    # Connect to DB
    connect(host=os.environ["MONGODB_URL"])

    # Dump data into DB article by article to prevet duplicates
    crawl_result = Crawler.execute(spider=ArticlesSpider)
    handled_articles = len(crawl_result)
    for article_elements in crawl_result:
        article = Article(**article_elements)
        try:
            article.save()
        except NotUniqueError:
            handled_articles -= 1

    return {"message": f"Retrieved {handled_articles} new elements."}