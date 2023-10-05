from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db.profile_crud import post_new_user
from ..profile_schema import Profile
#from .. import files

router = APIRouter(
    prefix="/profile", 
    tags=["profile"],
    responses={404: {"description": "Not Found"}}
    )

@router.post("/new-user/")
async def make_user_profile(uuid: str, username: str, gender: str, sex_pref: str, genre: str, bio: str):
    profile = Profile(
            uuid= uuid,
            username= username,
            gender= gender,
            sex_pref= sex_pref, ###########################THIS NEEDS TO BE CHANGED
            genre= genre,
            bio=bio,
        )
    response = post_new_user(profile = profile)
    if not response:
        raise HTTPException(status_code = 500, detail = "Error creating user")
    return {"message": "Profile created successfully"}
