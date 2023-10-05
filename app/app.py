from fastapi import FastAPI, APIRouter
from .routers import anime,users,database, profile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router: APIRouter = APIRouter()

origins = [
    "https://animatcher.xyz",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
