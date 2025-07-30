from pathlib import Path
from google.cloud import storage
import datetime
from rich import print


class Gcloud:
    def __init__(self, json_path: str):
        self.client = storage.Client.from_service_account_json(str(json_path))
        self.status = f"[green3]🐻‍❄️ Gcloud:[/]"
        self.bucket_name = "kevin-bi"
        self.bucket = self.client.bucket(self.bucket_name)

    def download_file(self, blob_path: str, file_path: Path):
        blob = self.bucket.blob(blob_path)
        blob.download_to_filename(file_path)
        print(f"{self.status} download {blob_path}")

    def upload_file(self, blob_path: str, file_path: Path):
        blob_path_full = f"{blob_path}/{file_path.name}"
        blob = self.bucket.blob(blob_path_full)
        blob.upload_from_filename(file_path)
        print(f"{self.status} upload {file_path.stem} to {blob_path}")
        return blob_path_full

    def generate_download_signed_url_v4(self, blob_file, minutes=15):
        blob = self.bucket.blob(blob_file)
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=minutes),
            method="GET",
        )
        print(f"{self.status} Presigned [{blob_file}] in {minutes} mins \nUrl: {url}")
        return url
