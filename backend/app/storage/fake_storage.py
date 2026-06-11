from app.storage.base import StorageBase


class FakeStorage(StorageBase):
    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        return f"https://fake-storage.com/{filename}"
