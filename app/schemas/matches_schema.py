from pydantic import BaseModel

class Matches(BaseModel):
    user_email: str 
    liked_email: str
