# coding: utf-8

import scrapy
import dateparser
from slugify import slugify
from dateutil.relativedelta import relativedelta


class ArticlesSpider(scrapy.Spider):
    name = 'articles-spider'
    start_urls = ['https://www.lemonde.fr/actualite-en-continu/']
    custom_settings = {"REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"}

    def parse(self, response):
        for article in response.css('section.teaser'):
            title = article.css("h3.teaser__title::text").get()

            publish_date = article.css("span.meta__date::text").get()
            publish_date = publish_date.replace("Publié", "")
            publish_datetime = dateparser.parse(publish_date.split(",")[0])

            yield {
                "slug": slugify(title),
                "title": title,
                "url": article.css("a.teaser__link::attr(href)").get(),
                "publish_date": publish_datetime,
                "author": article.css("span.meta__author::text").get()
            }
