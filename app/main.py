# coding: utf-8

from typing import Union
from fastapi import FastAPI

from .routers import scrapper, api

app = FastAPI(title="LeMonde articles")

app.include_router(scrapper.router)
app.include_router(api.router)