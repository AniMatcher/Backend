from fastapi import FastAPI, APIRouter
from .routers import database
from .routers import users

app = FastAPI()
router: APIRouter = APIRouter()

@app.get("/")
def hello_world():
	return {"hello": "world"}

#includes all the routers from the router folder
"""
	Steps to add router:
	1. add 'from .routers import *name of router file*
	2. under this write app.include_router(*imported filename*.router)
	Look below for example code
"""
app.include_router(database.router)
app.include_router(users.router)