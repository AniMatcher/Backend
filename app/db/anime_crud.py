from ..db import db_client 
from ..anime_schema import Anime

def post_anime(anime:Anime):
    return db_client.client.table("anime").insert({
        "anime_id": anime.anime_id, 
        "anime_name": anime.anime_name, 
        "score": anime.score,
        "genres": anime.genres,
        "type": anime.type
        }).execute()


