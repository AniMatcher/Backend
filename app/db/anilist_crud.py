from ..db import db_client 
from ..schemas.anime_schema import Anime

table = db_client.client.table("anilist_oauth") 

def add_anilist_token(uuid, token):
    return table.upsert({
        "uuid" : uuid,
        "token" : token
    }).execute()

def get_anilist_token(uuid: str):
    return table.select("*").eq("uuid", uuid).execute()
