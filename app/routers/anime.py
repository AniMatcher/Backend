from fastapi import FastAPI, APIRouter
import requests
import json
from ..anime_schema import Anime

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
    for id in range(1,50):
        url = f'https://api.jikan.moe/v4/anime/{id}/full'
        try:
            content = json.loads(requests.get(url).content)['data']
            vid_type = content['type'] #should be TV or Movie
            anime = Anime(
                mal_id=int(content['mal_id']),
                image=content['images']['jpg']['image_url'],
                anime_name=content['title'],
                vid_type=vid_type,
                score=float(content['score']),
                popularity=int(content['popularity']),
                synopsis=content['synopsis'],
                studio=content['studios'][0]['name'],
                funimation_url=content['streaming'][1]['url'],
                producer=content['producers'][0]['name']
            )
            animes.append(anime.model_dump_json())
        except:
            print(id)
    return animes