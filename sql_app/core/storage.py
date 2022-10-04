import os

import boto3
import botocore
from fastapi import Depends, UploadFile

from .config import Settings, get_settings


class Storage:
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.s3 = boto3.resource("s3")
        self.bucket_name = settings.aws_bucket_name
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.download_folder = "downloads"

    def generate_file_name(self, file_category: str, file_extension: str, file_name: str, owner_name: str) -> str:
        return f"{owner_name.replace(' ', '_')}/{file_category}/{file_name.replace(' ', '_')}{file_extension}"

    async def upload_file_to_s3(self, file: UploadFile, file_name: str):
        try:
            await self.bucket.upload_fileobj(file.file, file_name)
        except Exception as e:
            print("Something Happened: ", e)

    def download_music_from_s3(self, file_name: str):
        file_path = f"{self.download_folder}/{file_name.replace('/', '_')}"

        try:
            with open(file_path, 'wb') as f:
                self.bucket.download_fileobj(file_name, f)

                with open(file_path, "rb") as f:
                    yield from f
                    os.remove(file_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise e
