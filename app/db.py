# app/db.py

import databases
import ormar
import sqlalchemy

from datetime import datetime

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Articles(ormar.Model):
    class Meta(BaseMeta):
        tablename = "articles"

    slug: str = ormar.String(primary_key=True, max_length=256)
    title: str = ormar.String(max_length=256, unique=True, nullable=False)
    url: str = ormar.String(max_length=256, unique=True, nullable=False)
    author: str = ormar.String(max_length=128, nullable=False)
    publication_date: datetime = ormar.DateTime(nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
