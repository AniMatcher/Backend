from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db.profile_crud import post_new_user, user_animes
from ..db.crud import check_user_existence, get_user_by_uuid
from ..profile_schema import Profile, UserAnimesPost, UserAnimes
from pydantic import BaseModel
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

@router.get("/email/{email}")
async def get_user_profile(email: str):
    matched_users = check_user_existence(email)
    if not matched_users.data:
        raise HTTPException(status_code=500, detail="Email not found")
    else: 
        uuid = matched_users.data[0]["uuid"]
        return get_user_by_uuid(uuid=uuid).data[0]

@router.post("/new-user/")
async def make_user_profile(profile: PostProfile):
    matched_users = check_user_existence(profile.email)
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
    response = post_new_user(profile = profile)
    if not response:
        raise HTTPException(status_code = 500, detail = "Error creating user")
    return {"message": "Profile created successfully"}

@router.post("/animes/")
async def make_user_profile(profile: UserAnimesPost):
    matched_users = check_user_existence(profile.email)
    if not matched_users.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else:
        uuid = matched_users.data[0]["uuid"]
        uas = UserAnimes(uuid=uuid, animes=profile.animes)
        results =  user_animes(animes=uas)
        if not results:
            raise HTTPException(status_code = 500, detail = "Error creating user")
        return {"message": "Profile created successfully"}

