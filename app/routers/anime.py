from fastapi import FastAPI, APIRouter
import requests
import json
from ..anime_schema import Anime
from ..db.anime_crud import post_anime

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
        content = json.loads(requests.get(url).content)['data']
        vid_type = content['type'] #should be TV or Movie
        anime = Anime(
            anime_id=int(content['mal_id']),
            anime_name=content['title'],
            type= vid_type,
            genres="Romance", ###########################THIS NEEDS TO BE CHANGED
            score=float(content['score']),
            synopsis=content['synopsis'],
        )
        #print(anime)
        animes.append(anime.model_dump_json())
        post_anime(anime=anime)
    return animes