from fastapi import FastAPI, APIRouter
#from .. import files

router = APIRouter(
    prefix="/database", 
    tags=["database"],
    responses={404: {"description": "Not Found"}}
    )

@router.get("/")
def get_info():
    return "database"