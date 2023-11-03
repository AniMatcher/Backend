from fastapi import FastAPI, APIRouter
import requests
import json
from ..anime_schema import Anime
from ..db import anime_crud

router = APIRouter(
    prefix="/anime", 
    tags=["anime"],
    responses={404: {"description": "Not Found"}}
    )
# var options = {
#   uri: 'https://anilist.co/api/v2/oauth/token',
#   method: 'POST',
#   headers: {
#     'Content-Type': 'application/json',
#     'Accept': 'application/json',
#   },
#   json: {
#     'grant_type': 'authorization_code',
#     'client_id': '{client_id}',
#     'client_secret': '{client_secret}',
#     'redirect_uri': '{redirect_uri}', // http://example.com/callback
#     'code': '{code}', // The Authorization Code received previously
#   }
# };
@router.get("/token")
def get_anilist_token():
    url = 'https://anilist.co/api/v2/oauth/token'
    headers = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }
    client_id =''
    client_secret = ''
    redirect_uri = ''
    code = ''
    json = {
     'grant_type': 'authorization_code',
     'client_id': f'{client_id}',
     'client_secret': f'{client_secret}',
     'redirect_uri': f'{redirect_uri}', 
     'code': f'{code}'   
    }

@router.get("/")
def get_info(aid):
    return anime_crud.get_anime(aid=aid)

@router.post("/")
def add_anime_to_api(anime: Anime):
    anime_crud.post_anime(anime=anime)
    return anime
