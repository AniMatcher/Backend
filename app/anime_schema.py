from pydantic import BaseModel
from typing import Optional

class Anime(BaseModel):
    anime_id: int 
    anime_name: str 
    score: float
    genres: str
    synopsis: str 
    type: str