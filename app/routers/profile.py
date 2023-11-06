from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db import profile_crud, anime_crud, users_crud, auth_crud
from ..schemas.profile_schema import Profile, UserAnimesPost, UserAnimes
from pydantic import BaseModel
import requests
#from .. import files

router = APIRouter(
    prefix="/profile", 
    tags=["profile"],
    responses={404: {"description": "Not Found"}}
    )


class PostProfile(BaseModel):
    email: str
    gender: str
    sex_pref: str
    genre: str
    bio: str

@router.get("/uuid/{uuid}")
async def get_user_profile(uuid: str):
    '''
        Gets User Profile data from the Users Table + the images of the anime the user likes
    '''
    matched_users = auth_crud.check_uuid_user_existence(uuid)
    if not matched_users.data:
        raise HTTPException(status_code=500, detail="Email not found")
    else: 
        results =  profile_crud.get_user_animes(uuid).data
        aids = []
        for i in results:
            aids.append(i["aid"])
        temp_list = anime_crud.get_multiple_anime(aids).data
        image_urls = dict()
        for anime in temp_list:
            image_urls[anime["anime_name"]] = (anime["image_url"])
        profile_data = users_crud.get_user_by_uuid(uuid).data[0]
        profile_data['image_urls'] = image_urls
        return profile_data

@router.post("/new-user/")
async def make_user_profile(profile: PostProfile):
    matched_users = auth_crud.check_email_user_existence(profile.email)
    if not matched_users.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else:
        uuid = matched_users.data[0]["uuid"]
        username = matched_users.data[0]["username"]
        profile = Profile(
            uuid= uuid,
            username= username,
            gender= profile.gender,
            sex_pref= profile.sex_pref, 
            genre= profile.gender,
            bio=profile.bio,
        )
    response = users_crud.post_new_user(profile = profile)
    if not response:
        raise HTTPException(status_code = 500, detail = "Error creating user")
    return {"message": "Profile created successfully"}

@router.post("/animes/")
async def make_user_animes(profile: UserAnimesPost):
    matched_users = auth_crud.check_email_user_existence(profile.email)
    if not matched_users.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else:
        uuid = matched_users.data[0]["uuid"]
        uas = UserAnimes(uuid=uuid, animes=profile.animes)
        results =  profile_crud.post_user_animes(animes=uas)
        if not results:
            raise HTTPException(status_code = 500, detail = "Error creating user")
        return {"message": "Profile created successfully"}

@router.get("/animes/")
async def get_user_anime(uuid: str):
    matched_users = auth_crud.check_uuid_user_existence(uuid)
    if not matched_users.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else:
        results =  profile_crud.get_user_animes(uuid).data
        aids = []
        for i in results:
            aids.append(i["aid"])
        temp_list = anime_crud.get_multiple_anime(aids).data
        image_url_list = []
        for anime in temp_list:
            image_url_list.append(anime["image_url"])
        return image_url_list

