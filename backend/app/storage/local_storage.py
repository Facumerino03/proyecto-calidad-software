import os
import uuid
from pathlib import Path

from app.config import get_settings
from app.storage.base import StorageBase


class LocalStorage(StorageBase):
    def __init__(self):
        settings = get_settings()
        self.base_path = Path(settings.storage_path)
        self.base_url = settings.storage_base_url.rstrip("/")
        self.base_path.mkdir(parents=True, exist_ok=True)

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        ext = Path(filename).suffix or ""
        file_id = f"arch-{uuid.uuid4().hex[:12]}"
        stored_name = f"{file_id}{ext}"
        file_path = self.base_path / stored_name
        file_path.write_bytes(file_content)
        return f"{self.base_url}/{file_id}{ext}"
