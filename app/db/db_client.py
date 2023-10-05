import os
from supabase import create_client, Client



url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
client: Client = create_client("https://hghehkvmtmkxmjppybvp.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnaGVoa3ZtdG1reG1qcHB5YnZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYzNjcxMDMsImV4cCI6MjAxMTk0MzEwM30.wtQJPuDKo2hY2z80aZqouIURUolu1LVW6C7mFhuQlgs")