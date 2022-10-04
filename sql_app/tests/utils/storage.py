from fastapi import UploadFile


class OverrideStorage:
    def __init__(self):
        self.download_folder = "sql_app/tests/fixtures/files"

    def generate_file_name(self, file_category: str, file_type: str, file_name: str, owner_name: str) -> str:
        return f"{owner_name.replace(' ', '_')}/{file_category}/{file_name.replace(' ', '_')}{file_type}"

    async def upload_file_to_s3(self, _file: UploadFile, _file_name: str):
        return

    def download_music_from_s3(self, file_name: str):
        file_path = f"{self.download_folder}/{file_name.replace('/', '_')}"
        with open(file_path, "rb") as f:
            yield from f
