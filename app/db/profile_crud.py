from ..db import db_client 
from ..schemas.profile_schema import Profile, UserAnimes

def post_user_animes(animes: UserAnimes):
    data = [{"uuid": animes.uuid, "aid": anime} for anime in animes.animes]
    return db_client.client.table("user_animes").insert(data).execute()

def get_user_animes(uuid: str):
    return db_client.client.table("user_animes").select("aid").eq("uuid", uuid).execute()

def get_profile(uuid: str):
    return db_client.client.rpc('get_user_profile', {'user_id': uuid}).execute()