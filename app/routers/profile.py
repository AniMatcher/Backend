from fastapi import FastAPI, APIRouter
import requests
import json
#from .. import files

router = APIRouter(
    prefix="/profile", 
    tags=["profile"],
    responses={404: {"description": "Not Found"}}
    )

@router.post("/")
def make_user_profile():
    pass