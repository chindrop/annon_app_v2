import boto3
from botocore.client import Config
from os import getenv

def configure_boto():
    boto_session = boto3.Session( 
        aws_access_key_id = getenv('AWS_ACCESS_KEY_ID'), 
        aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY'),
        region_name = getenv('AWS_REGION')
        )
    s3 = boto_session.resource('s3')
    bucket = s3.Bucket('blackbird-audio-files')
    s3_client = boto_session.client('s3', 'eu-central-1',config=Config(signature_version='s3v4'))

    return boto_session, bucket, s3_client



    