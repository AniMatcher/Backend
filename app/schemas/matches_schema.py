from pydantic import BaseModel

class Matches(BaseModel):
    uuid: str 
    liked_uuid: str
