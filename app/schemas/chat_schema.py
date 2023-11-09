from pydantic import BaseModel
from typing import Optional
import datetime

class Chat(BaseModel):
    id: int
    created_at: datetime.datetime
    chat_id: str
    member_a: str
    member_b: str