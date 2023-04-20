# coding: utf-8

import scrapy
import dateparser


class ArticlesSpider(scrapy.Spider):
    name = 'articles-spider'
    start_urls = ['https://www.lemonde.fr/actualite-en-continu/']
    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    def parse(self, response):
        for article in response.css('section.teaser'):
            publication_date = article.css("span.meta__date::text").get()
            publication_date = publication_date.replace("Publié", "")
            publication_datetime = dateparser.parse(
                publication_date.split(",")[0]
            )

            yield {
                "title": article.css("h3.teaser__title::text").get(),
                "url": article.css("a.teaser__link::attr(href)").get(),
                "author": article.css("span.meta__author::text").get(),
                "description": article.css("p.teaser__desc::text").get(),
                "publication_date": publication_datetime
            }
