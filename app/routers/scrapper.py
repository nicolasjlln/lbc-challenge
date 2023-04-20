# coding: utf-8

import os

from fastapi import APIRouter

from app.spiders import ArticlesSpider
from app.crawler import Crawler

# from app.db import database, Articles
from app.database.models import Article
# from app.database import client as mongo_client
from mongoengine import connect


router = APIRouter(prefix="/scrapper", tags=["Scrapper"])

@router.post("/retrieve_articles")
async def retrieve_articles():
    # runner.crawl(ArticlesSpider)
    # result = runner.join()

    connect(db="lbc", host=os.environ["MONGODB_URL"])

    
    # db = mongo_client.lbc
    # articles = db.articles
    # articles.insert_many(result)
    crawl_result = Crawler.execute(spider=ArticlesSpider)
    for article_elements in crawl_result:
        article = Article(**article_elements)
        print(article.to_mongo())
        article.save()
    
    
    # if not database.is_connected:
    #     await database.connect()
    # for item in result:
    #     Articles.objects.bulk_create
    # return result#{"Status": "OK"}
    return {"message": f"Retrieved {len(crawl_result)} elements."}