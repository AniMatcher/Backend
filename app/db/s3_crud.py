from ..db import s3bucket_client
#import s3bucket_client
import boto3 
client = s3bucket_client.client
bucket_name: str = s3bucket_client.bucket
tag_key = 'public'
tag_value = 'yes'

def upload_image(file: bytes, store_as: str) -> str:
    res = client.upload_fileobj(file, bucket_name, store_as)
    client.put_object_tagging(Bucket=bucket_name, Key=store_as, Tagging={
            'TagSet': [{"Key": tag_key, "Value" : tag_value}]
    })
    location = client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    url = f"https://animatcher.s3.amazonaws.com/{store_as}"
    return url


def download_image(path_to_download, save_as=None):
    '''
        path_to_download: filename in s3 bucket that you want to download
        save_as: the filename you want to save as for local use
    '''
    if save_as == None:
        save_as = path_to_download
    try:
        client.download_file(bucket_name, path_to_download, save_as)
    except:
        raise Exception("Unable to download this file")

def check_object_exist(object):
    try:
        client.head_object(Bucket=bucket_name, Key=object)
        return True 
    except:
        return False

def get_object_url(object) -> str:
    '''
        Gets the object url from an s3 bucket. The object file is the file name of the row in s3 bucket
    '''
    if check_object_exist(object):
        return f"https://animatcher.s3.amazonaws.com/{object}"
    else:
        raise Exception("File doesn't exist in bucket")