from fastapi import FastAPI, APIRouter
import requests
import json
#from .. import files

router = APIRouter(
    prefix="/login", 
    tags=["login"],
    responses={404: {"description": "Not Found"}}
    )
