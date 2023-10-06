from pydantic import BaseModel
from typing import Optional

class Profile(BaseModel):
    uuid: str
    username: str
    gender: str
    sex_pref: str
    genre: str
    bio: str

class UserAnimesPost(BaseModel):
    email: str
    animes: list[str]

class UserAnimes(BaseModel):
    uuid: str
    animes: list[str]