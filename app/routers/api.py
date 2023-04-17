# coding: utf-8

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Api"])


@router.get("/articles")
def articles():
    return {"message": "Hello"}