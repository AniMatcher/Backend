from pydantic import BaseModel
from typing import Optional

class Profile(BaseModel):
    uuid: str
    username: str
    gender: str
    sex_pref: str
    genre: str
    bio: str