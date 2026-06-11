import pytest
from fastapi import HTTPException

from app.services import archivo as service
from app.storage.fake_storage import FakeStorage

MAX_SIZE = 10 * 1024 * 1024


class TestArchivoServices:

    def test_subir_pdf(self, archivo_repo):
        file = ("factura.pdf", b"%PDF-1.4 content", "application/pdf")
        storage = FakeStorage()
        result = service.subir_archivo(file, storage, archivo_repo)
        assert result.id.startswith("arch-")
        assert result.tipo_mime == "application/pdf"

    def test_subir_imagen_jpg(self, archivo_repo):
        file = ("dni.jpg", b"\xff\xd8\xff jpeg content", "image/jpeg")
        storage = FakeStorage()
        result = service.subir_archivo(file, storage, archivo_repo)
        assert result.id.startswith("arch-")
        assert result.tipo_mime == "image/jpeg"

    def test_subir_tipo_no_permitido(self, archivo_repo):
        file = ("archivo.gif", b"GIF89a", "image/gif")
        storage = FakeStorage()
        with pytest.raises(HTTPException) as exc:
            service.subir_archivo(file, storage, archivo_repo)
        assert exc.value.status_code == 415

    def test_subir_archivo_muy_grande(self, archivo_repo):
        large_content = b"x" * (MAX_SIZE + 1)
        file = ("grande.pdf", large_content, "application/pdf")
        storage = FakeStorage()
        with pytest.raises(HTTPException) as exc:
            service.subir_archivo(file, storage, archivo_repo)
        assert exc.value.status_code == 413
