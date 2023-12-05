from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db import users_crud, auth_crud, matches_crud, profile_crud,anime_crud
from ..schemas.matches_schema import Matches
from pydantic import BaseModel
import random
#from .. import files

router = APIRouter(
    prefix="/user", 
    tags=["user"],
    responses={404: {"description": "Not Found"}}
    )


@router.get("/mutuals/")
def get_potential_mutuals(uuid:str):
    user_data = auth_crud.check_uuid_user_existence(uuid)
    if not user_data.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    resp = matches_crud.get_mutuals(uuid).data
    user_data = []
    for match in resp:  
        user_uuid = match['liked_user']
        user_data.append(dict(users_crud.get_user_by_uuid(user_uuid)))
    return {"matches": user_data}


@router.post("/matches")
def like_user(match: Matches):
    '''
        Allows a current user to like another person on the potential list of people
    '''
    user_data = auth_crud.check_uuid_user_existence(match.uuid)
    foreign_user_data = auth_crud.check_uuid_user_existence(match.liked_uuid)
    if not user_data.data or not foreign_user_data.data:
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else: 
        user_uuid = match.uuid
        foreign_uuid = match.liked_uuid

        foreign_liked_users = matches_crud.get_user_liked(foreign_uuid).data #list of people the person you liked likes
        for i in range(len(foreign_liked_users)):
            uid = foreign_liked_users[i]['liked_user']
            foreign_liked_users[i] = uid #auth_crud.get_email_from_uuid(uid).data[0]['email']
        if user_uuid in foreign_liked_users: #if the foreign user has liked the current user they match
            matches_crud.create_user_liked(user_uuid, foreign_uuid, True)
        else: # the foreign user has not liked the current user so the current user likes the foreign user
            matches_crud.create_user_liked(user_uuid, foreign_uuid, False)


@router.get("/matches")
def get_potential_matches(uuid:str, num:int):
    '''
        Returns a list of matches given a UUID of the person
    '''
    user_data = auth_crud.check_uuid_user_existence(uuid)
    if not user_data.data: 
        raise HTTPException(status_code = 500, detail = "Error invalid email")
    else:
        sex_pref = users_crud.get_user_by_uuid(uuid).data[0]['sex_pref']
        uuid_gender =  []
        if sex_pref == 'A':
            uuid_gender.append('M')
        elif sex_pref == 'B':
            uuid_gender.append('F')
        elif sex_pref == 'D':
            uuid_gender.append('NB')
        elif sex_pref == 'C':
            uuid_gender.append('M')
            uuid_gender.append('F')
        elif sex_pref == 'E':
            uuid_gender.append('M')
            uuid_gender.append('NB')
        elif sex_pref == 'F':
            uuid_gender.append('F')
            uuid_gender.append('NB')
        elif sex_pref == 'G':
            uuid_gender.append('M')
            uuid_gender.append('F')
            uuid_gender.append('NB')
        
        user_liked_list = []
        for genders in uuid_gender:
            desired = users_crud.get_all_desired_user(genders, uuid).data
            for i in range( min(int(num / len(uuid_gender)), len(desired))):
                desired[i]['image_urls'] = desired[i]['image_urls'].replace("{","").replace("}","").split(",")
                user_liked_list.append(desired[i])

        if len(user_liked_list) == 0:
            raise HTTPException(status_code=500, detail="no potential matches")
        else:
            random.shuffle(user_liked_list)
            return user_liked_list

@router.get("/uuid/{uuid}")
def get_user(uuid: str):
    '''
        Gets user information based on uuid
    '''
    user_data = users_crud.get_user_by_uuid(uuid)
    #print(uuid, user_data)
    if not user_data.data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.get("/email/{uuid}")
def check_user(email: str):
    '''
        check if a user exists based on email. MUST BE EMAIL
    '''
    user_data = auth_crud.check_email_user_existence(email)
    if user_data.data:
        return {"status": True} 
    return {"status": False} 

class UserAuthPost(BaseModel):
    email: str
    username: str
    password_hash: str

@router.post("/")
def create_user_auth(auth_body: UserAuthPost):
    '''
        Creates a user in the auth table based on email, username, & password
    '''
    response = auth_crud.post_user_auth( auth_body.email, auth_body.username, auth_body.password_hash)
    if not response:
        raise HTTPException(status_code=500, detail="Error creating user")
    return {"message": "User created successfully"}







