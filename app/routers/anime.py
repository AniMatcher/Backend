from fastapi import FastAPI, APIRouter
import requests
import json
#from .. import files

router = APIRouter(
    prefix="/anime", 
    tags=["anime"],
    responses={404: {"description": "Not Found"}}
    )

@router.get("/")
def get_info():
    return "but"

@router.post("/")
def add_anime_to_api():
    animes = []
    for id in range(1,2):
        url = f'https://api.jikan.moe/v4/anime/{id}/full'
        animes.append(json.loads(requests.get(url).content))
    return animes