from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db import profile_crud, anime_crud, users_crud, auth_crud, s3_crud, matches_crud
from ..schemas.profile_schema import Profile, UserAnimesPost, UserAnimes, UserProfileImage
from pydantic import BaseModel
import requests
import boto3 
from botocore.vendored import requests
from io import BytesIO
from datetime import datetime
import base64
from ..db import chat_crud
import json
#from .. import files

router = APIRouter(
    prefix="/chat", 
    tags=["chats"],
    responses={404: {"description": "Not Found"}}
    )


class ChatCreate(BaseModel):
    user_a: str
    user_b: str

@router.post("/chat/")
async def create_chat(data: ChatCreate):
    '''
        Gets User Profile data from the Users Table + the images of the anime the user likes
    '''
    try:
        out = chat_crud.create_new_chat(data.user_a, data.user_b)
    except Exception as e:
        print(e)
        return {"error": str(e)}, 400
    else:
        return out.data[0]

@router.get("/user-chats/")
async def create_chat(uuid: str):
    '''
        Gets User Profile data from the Users Table + the images of the anime the user likes
    '''
    try:
        out = chat_crud.get_user_chats(uuid)
    except Exception as e:
        return {"error": str(e)}
    else:
        return {"data": out}


@router.get("/mutuals-with-chats/")
def get_potential_matches(uuid:str):
    '''
        checks to make sure each chatroom is with a mutally matched person. then it creates a dict of who matches with who
    '''
    user_data = auth_crud.check_uuid_user_existence(uuid)
    if not user_data.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    
    resp = matches_crud.get_mutuals(uuid).data
    user_data = []
    use_chat_data = []
    print(resp)
    out = chat_crud.get_user_chats(uuid)
    print(out)

    if len(resp) < 1:
        return  {"matches": [], "chats": []}

    for match in resp:
        user_uuid = match['liked_user']
        has_chat = None
        for itm in out:
            if (itm["member_b"] == user_uuid and uuid == itm["member_a"])  or (itm["member_a"] == user_uuid and uuid == itm["member_b"]):
                has_chat = itm
                break
        profile = dict(users_crud.get_user_by_uuid(user_uuid).data[0])
        if has_chat:
            profile["chat_id"] = has_chat["chat_id"]
            use_chat_data.append(profile)
        else:
            user_data.append(profile)
    
   

    return {"matches": user_data, "chats": use_chat_data}


