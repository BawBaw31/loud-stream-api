import boto3
from fastapi import Depends, UploadFile
from sql_app.core.config import Settings
from sql_app.core.database import get_settings


class Storage:
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.bucket_name = settings.aws_bucket_name

    def upload_file_to_s3(self, file: UploadFile) -> str:
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucket_name)
        try:
            bucket.upload_fileobj(file.file, file.filename)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file.filename}"
        except Exception as e:
            print("Something Happened: ", e)
            return False
