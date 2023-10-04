from pydantic import BaseModel
from typing import Optional

class Anime(BaseModel):
    mal_id: int 
    image: str 
    anime_name: str 
    vid_type: str 
    score: float
    popularity: int 
    synopsis: str 
    studio: str 
    funimation_url: Optional[str]
    producer: Optional[str]
