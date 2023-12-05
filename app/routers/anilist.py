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

class WatchDataReq(BaseModel):
    uuid: str
    count: int
    meanScore: float
    minutesWatched: int
    episodesWatched: int

router = APIRouter(
    prefix="/anilist", 
    tags=["anilist"],
    responses={404: {"description": "Not Found"}}
    )

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
    #print(body)
    res = requests.post(url = 'https://anilist.co/api/v2/oauth/token', json = body)
    if (res.status_code == 200):
        token = res.json()
        access_token = token["access_token"]
        anilist_crud.add_anilist_token(uuid=uuid, token=access_token)
        user_data = get_user_info(uuid)
        if user_data["data"]:
            path = user_data["data"]["Viewer"]["statistics"]["anime"]
            anilist_crud.add_user_metrics(uuid, True, path["count"], path["meanScore"], path["minutesWatched"], path["episodesWatched"])
            return {"token": token['access_token']}
        else:
            return {"error": "exception"}, 500
    else: 
        token = res.json()
        #print(token)
        return {"error": "exception"}, 500
    

@router.post("/user/")
def get_user_info(watch_data: WatchDataReq):
    anilist_crud.add_user_metrics(watch_data.uuid, False, watch_data.count, watch_data.meanScore, watch_data.minutesWatched, watch_data.episodesWatched)
    return {"data": "prev o"}

# @router.get("/user/{uuid}")
def get_user_info(uuid: str):
    token = anilist_crud.get_anilist_token(uuid).data[0]["token"]
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
    response = requests.post(uri, headers= headers, json={'query': query})
    json_d = response.json()
    return json_d