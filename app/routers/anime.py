from fastapi import FastAPI, APIRouter
import requests
import json
from ..schemas.anime_schema import Anime
from ..db import anime_crud

router = APIRouter(
    prefix="/anime", 
    tags=["anime"],
    responses={404: {"description": "Not Found"}}
    )

@router.get("/")
def get_info(aid):
    return anime_crud.get_anime(aid=aid)

@router.post("/")
def add_anime_to_api(anime: Anime):
    anime_crud.post_anime(anime=anime)
    return anime
