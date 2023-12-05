from ..db import db_client 
from ..schemas.anime_schema import Anime

table = db_client.client.table("anilist_oauth") 
metrics_table = db_client.client.table("user_metrics")

def add_anilist_token(uuid, token):
    return table.upsert({
        "uuid" : uuid,
        "token" : token
    }).execute()

def get_anilist_token(uuid: str):
    return table.select("*").eq("uuid", uuid).execute()

def add_user_metrics(uuid: str, anilist: bool, count: int, meanScore: float, minutesWatched: float, episodesWatched: float):
    return metrics_table.upsert({
        "uuid": uuid,
        "anilist": anilist,
        "count": count,
        "meanScore": meanScore,
        "minutesWatched": minutesWatched,
        "episodesWatched": episodesWatched
    }).execute()

def get_user_metrics(uuid: str):
    return metrics_table.select("*").eq("uuid", uuid).execute()