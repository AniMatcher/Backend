from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db import profile_crud, anime_crud, users_crud, auth_crud, s3_crud, anilist_crud
from ..schemas.profile_schema import Profile, UserAnimesPost, UserAnimes, UserProfileImage
from pydantic import BaseModel
import requests
import boto3 
from botocore.vendored import requests
from io import BytesIO
from datetime import datetime
import base64
import json
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
    image: str
    image_name: str

class MockProfile(BaseModel):
    email: str
    gender: str
    sex_pref: str
    genre: str
    bio: str
    image_url: str

class Blog(BaseModel):
    uuid: str 
    blog: str 

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
        metrics = anilist_crud.get_user_metrics(uuid).data
        if len(metrics) >= 1:
            profile_data['metrics'] = metrics
        return profile_data

@router.post("/new-user/")
async def make_user_profile(profile: PostProfile):
    '''
        Creates the user profile with the profile image as well
    '''
    matched_users = auth_crud.check_email_user_existence(profile.email)
    if not matched_users.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else:
        uuid = matched_users.data[0]["uuid"]
        username = matched_users.data[0]["username"]
        s3 = boto3.resource('s3')
        img_data = BytesIO(base64.b64decode(profile.image.split(";base64,", 1)[1])) #read image bytes
        img_data.seek(0) #resets the buffer
        bucket_name = ""
        file_name = f"{uuid}_{datetime.now().isoformat().replace(' ','')}.{profile.image_name.split('_')[0].split('.')[1]}"
        print(file_name)
        url = s3_crud.upload_image(img_data, file_name)
        print(url)
        profile = Profile(
            uuid=uuid,
            username= username,
            gender= profile.gender,
            sex_pref= profile.sex_pref, 
            genre= profile.genre,
            bio=profile.bio,
            image=url
        )
        response = users_crud.post_new_user(profile = profile)
        if not response:
            raise HTTPException(status_code = 500, detail = "Error creating user")
        return {"message": "Profile created successfully"}

@router.post("/blog/")
async def make_blog_post(blog: Blog):
    try: 
        users_crud.post_blog(blog.blog, blog.uuid)
    except:
        return HTTPException(status_code = 500, detail = "Error making blog")

@router.get("/blog/{uuid}")
async def get_blog_post(uuid):
    try: 
        return users_crud.get_blog(uuid)
    except:
        return HTTPException(status_code = 500, detail = "Error getting blog")

@router.post("/mock-user/")
async def make_mock_user_profile(profile: MockProfile):
    '''
        Creates fake profile so we can differentiate who is real and allow the bots to have an AI Chatbot with ti
    '''
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
            genre= profile.genre,
            bio=profile.bio,
            image=profile.image_url
        )
        response = users_crud.post_new_user(profile = profile, fake=True)
        if not response:
            raise HTTPException(status_code = 500, detail = "Error creating user")
        return {"message": "Profile created successfully"}

@router.post("/edit-profile/")
async def edit_user_profile(profile: Profile):
    '''
        Allows users to edit the profile 
    '''
    response = users_crud.put_edit_user(profile = profile)
    if not response:
        raise HTTPException(status_code = 500, detail = "Error creating user")

@router.post("/animes/")
async def make_user_animes(profile: UserAnimesPost):
    """
        Creates a liked anime profile given the UserAnimesPost schema
    """
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
    """
        Gets the users preferred anime
        Return: list of image urls
    """
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


