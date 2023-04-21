# coding: utf-8

import os

from fastapi import APIRouter

from app.crawler import Crawler
from app.spiders import ArticlesSpider
from app.database.documents import Article

from mongoengine import connect
from mongoengine.errors import NotUniqueError


router = APIRouter(prefix="/scrapper", tags=["Scrapper"])

spider_crawler = Crawler(spider=ArticlesSpider)

@router.post("/retrieve_articles")
async def retrieve_articles():
    """Retrieve articles from the ArticleSpider result towards the database."""
    # Connect to DB
    connect(host=os.environ["MONGODB_URL"])

    # Dump data into DB article by article to prevet duplicates
    crawl_result = spider_crawler.execute()
    handled_articles = len(crawl_result)
    for article_elements in crawl_result:
        article = Article(**article_elements)
        try:
            article.save()
        except NotUniqueError:
            handled_articles -= 1

    # Return the number of collected new articles.
    return {"message": f"Retrieved {handled_articles} new elements."}