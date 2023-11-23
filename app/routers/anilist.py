from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response, Header
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from ..db import profile_crud, anime_crud, users_crud, auth_crud, s3_crud
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
    redirect_uri = "http://127.0.0.1:5000/anilist/redirect"
    return f"""<a href='https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'>Login with AniList</a>"""
@router.get("/redirect")
def create_token(response: Response, code: str):
    client_id = os.getenv("ANILIST_CLIENT_ID")
    client_secret = os.getenv("ANILIST_SECRET")
    redirect_uri = "http://127.0.0.1:5000/anilist/redirect"
    body = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    token = json.loads(requests.post(url = 'https://anilist.co/api/v2/oauth/token', json = body).content)
    response.set_cookie(key="ANILIST_TOKEN", value=token['access_token'])
    return token['access_token']

@router.get("/user")
def get_user_info(request: Request):
    token = get_token(request=request)
    uri = 'https://graphql.anilist.co'
    headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    query = '''
    query { # Define which variables will be used in the query (id)
    Viewer { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
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

def get_token(request: Request):
    token = request.cookies.get("ANILIST_TOKEN")
    if token == None:
        return RedirectResponse("http://127.0.0.1:5000/anilist")
    else: 
        return token