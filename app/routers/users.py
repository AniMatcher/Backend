from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db import users_crud, auth_crud
from pydantic import BaseModel
#from .. import files

router = APIRouter(
    prefix="/user", 
    tags=["user"],
    responses={404: {"description": "Not Found"}}
    )

@router.get("/uuid/{uuid}")
def get_user(uuid: str):
    user_data = users_crud.get_user_by_uuid(uuid)
    print(uuid, user_data)
    if not user_data.data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.get("/email/{email}")
def check_user(email: str):
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
    response = auth_crud.post_user_auth( auth_body.email, auth_body.username, auth_body.password_hash)
    if not response:
        raise HTTPException(status_code=500, detail="Error creating user")
    return {"message": "User created successfully"}








