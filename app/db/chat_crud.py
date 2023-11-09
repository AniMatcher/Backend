from ..db import db_client 
from ..schemas.profile_schema import Profile


table = db_client.client.table("chats")

def create_new_chat(uuid: str, member_uuid: str):
    return table.insert({
        "member_a": uuid,
        "member_b": member_uuid,
    }).execute()

def get_user_chats(uuid: str):
    return table.select("*").eq("member_a", uuid).execute()
