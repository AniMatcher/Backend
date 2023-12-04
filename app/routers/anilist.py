from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response, Header
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from ..db import profile_crud, anime_crud, users_crud, auth_crud, s3_crud, anilist_crud
from ..schemas.profile_schema import Profile, UserAnimesPost, UserAnimes, UserProfileImage
from pydantic import BaseModel
import requests
from datetime import datetime
import base64
import json
#from .. import files
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/anilist", 
    tags=["anilist"],
    responses={404: {"description": "Not Found"}}
    )

@router.get("/", response_class=HTMLResponse)
def index():
    client_id = os.getenv("ANILIST_CLIENT_ID")
    client_secret = os.getenv("ANILIST_SECRET")
    redirect_uri = os.getenv("ANILIST_REDIRECT_URI")
    return f"""<a href='https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'>Login with AniList</a>"""

@router.post("/redirect")
def create_token(code: str, uuid: str):
    client_id = os.getenv("ANILIST_CLIENT_ID")
    client_secret = os.getenv("ANILIST_SECRET")
    redirect_uri = os.getenv("ANILIST_REDIRECT_URI")
    body = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    token = json.loads(requests.post(url = 'https://anilist.co/api/v2/oauth/token', json = body).content)
    anilist_crud.add_anilist_token(uuid=uuid, token=token)
    return token['access_token']

@router.get("/user/{token}")
def get_user_info(token):
    uri = 'https://graphql.anilist.co'
    headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    query = '''
    query { 
    Viewer { 
        name,
        avatar {
            large
        },
        statistics {
            anime {
                count,
                meanScore,
                minutesWatched,
                episodesWatched,
                
            }
        },
        siteUrl,

    }
    }
    '''
    # Make the HTTP Api request
    response = json.loads(requests.post(uri, headers= headers, json={'query': query}).content)
    return response