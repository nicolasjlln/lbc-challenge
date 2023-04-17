# coding: utf-8

from fastapi import APIRouter

router = APIRouter(prefix="/scrapper", tags=["Scrapper"])


@router.post("/retrieve_articles")
def retrieve_articles():
    return {"message": "Hello"}