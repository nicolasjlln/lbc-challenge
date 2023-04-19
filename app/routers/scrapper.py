# coding: utf-8

from fastapi import APIRouter

from app.spiders import ArticlesSpider
from scrapy.crawler import CrawlerRunner

from app.db import database, Articles


router = APIRouter(prefix="/scrapper", tags=["Scrapper"])

runner = CrawlerRunner()


@router.post("/retrieve_articles")
async def retrieve_articles():
    result = runner.crawl(ArticlesSpider)
    if not database.is_connected:
        await database.connect()
    for item in result:
        Articles.objects.bulk_create
    return result#{"Status": "OK"}