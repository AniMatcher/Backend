import os
import boto3
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY: str = os.getenv("AWS_S3_ACCESS_KEY")
SECRET_KEY: str = os.getenv("AWS_S3_SECRET_ACCESS_KEY")

client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
bucket = "animatcher"
