from ..db import db_client 

table = db_client.client.table("auth")

def check_email_user_existence(email: str):
    return table.select("*").eq("email", email).execute()

def check_uuid_user_existence(uuid: str):
    return table.select("*").eq("uuid", uuid).execute()

def post_user_auth(email: str, username: str, password_hash: str):
    return table.insert({"email": email, "username": username, "password_hash": password_hash}).execute()

def get_uuid_from_email(email: str):
    return table.select("uuid").eq("email", email).execute()

def get_email_from_uuid(uuid: str):
    return table.select("email").eq("uuid", uuid).execute()
