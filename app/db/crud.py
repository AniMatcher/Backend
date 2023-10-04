from ..db import db_client 

def get_user_by_uuid(uuid: str):
    return db_client.client.table("Users").select("*").eq("uuid", uuid).execute()

def check_user_existence(email: str):
    return db_client.client.table("auth").select("*").eq("email", email).execute()

def post_user_auth(uuid: str, email: str, username: str, password_hash: str):
    return db_client.client.table("Auth").insert({"uuid": uuid, "email": email, "username": username, "password_hash": password_hash}).execute()

