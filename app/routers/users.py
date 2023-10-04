from fastapi import FastAPI, APIRouter, Depends, HTTPException
from ..db.crud import get_user_by_uuid, check_user_existence, post_user_auth
#from .. import files

router = APIRouter(
    prefix="/user", 
    tags=["user"],
    responses={404: {"description": "Not Found"}}
    )

@router.get("/uuid/{uuid}")
def get_user(uuid: str):
    user_data = get_user_by_uuid(uuid)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.get("/email/{email}")
def check_user(email: str):
    user_data = check_user_existence(email)
    if user_data is None:
        return {"status": False} 
    return {"status": True} 

@router.post("/")
def create_user_auth(uuid: str, email: str, username: str, password_hash: str):
    response = post_user_auth(uuid, email, username, password_hash)
    if response is None:
        raise HTTPException(status_code=500, detail="Error creating user")
    return {"message": "User created successfully"}








