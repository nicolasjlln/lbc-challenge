# coding: utf-8

from datetime import datetime
from mongoengine import Document, StringField, DateTimeField

class Article(Document):
    # meta = {'db_alias': 'articles'}

    title = StringField(
        max_length=256, required=True, unique_with="publication_date"
    )
    url = StringField(max_length=256, required=True)
    author = StringField(max_length=128, required=True)
    description = StringField(max_length=2048, required=True)
    publication_date = DateTimeField(required=True, unique_with="title")
    creation_date = DateTimeField(default=datetime.utcnow)