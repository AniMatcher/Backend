from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db.profile_crud import post_new_user
from ..db.crud import check_user_existence
from ..profile_schema import Profile
#from .. import files

router = APIRouter(
    prefix="/profile", 
    tags=["profile"],
    responses={404: {"description": "Not Found"}}
    )

@router.post("/new-user/")
async def make_user_profile(email: str, gender: str, sex_pref: str, genre: str, bio: str):
    matched_users = check_user_existence(email)
    if not matched_users.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else:
        uuid = matched_users.data[0]["uuid"]
        username = matched_users.data[0]["username"]
    profile = Profile(
            uuid= uuid,
            username= username,
            gender= gender,
            sex_pref= sex_pref, 
            genre= genre,
            bio=bio,
        )
    response = post_new_user(profile = profile)
    if not response:
        raise HTTPException(status_code = 500, detail = "Error creating user")
    return {"message": "Profile created successfully"}
