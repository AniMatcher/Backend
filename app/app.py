from fastapi import FastAPI, APIRouter
from .routers import anime,users,database, profile
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()
router: APIRouter = APIRouter()

@app.get("/")
def hello_world():
	return {"hello": "world"}



@app.exception_handler(500)
async def internal_server_error(req, exc):
    e_str = str(exc)
    return JSONResponse(status_code=500,
                        content={
                            "message": "Internal Server Error",
                            "error": e_str
                        })

#includes all the routers from the router folder
"""
	Steps to add router:
	1. add 'from .routers import *name of router file*
	2. under this write app.include_router(*imported filename*.router)
	Look below for example code
"""
app.include_router(database.router)
app.include_router(users.router)
app.include_router(anime.router)
app.include_router(profile.router)
