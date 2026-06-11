from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageBase(ABC):
    @abstractmethod
    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        """Upload file and return URL."""
