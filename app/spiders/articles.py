# coding: utf-8

import scrapy
from slugify import slugify
from datetime import date
from dateutil.relativedelta import relativedelta

class ArticlesSpider(scrapy.Spider):
    name = 'articles-spider'
    start_urls = ['https://www.lemonde.fr/actualite-en-continu/']

    def parse(self, response):
        for article in response.css('section.teaser'):
            title = article.css("h3.teaser__title::text").get()

            publish_date = article.css("span.meta__date::text").get()
            if "aujourd'hui" in publish_date:
                publish_datetime = date.today()
            elif "hier" in publish_date:
                publish_datetime = date.today() - relativedelta(days=1)

            yield {
                "slug": slugify(title),
                "title": title,
                "url": article.css("a.teaser__link::attr(href)").get(),
                "publish_date": publish_date,
                "author": article.css("span.meta__author::text").get()
            }
        # for article in response.xpath('//div[@id="river"]'):
        #     yield {'article': article.xpath('/section/a::text').get()}

        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)