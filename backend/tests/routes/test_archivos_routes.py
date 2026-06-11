from datetime import datetime, timezone

from app.schemas.archivo import ArchivoResponse


class TestArchivosRoutes:

    def test_subir_pdf_201(self, client, mocker):
        mocker.patch(
            "app.routes.archivos.service.subir_archivo",
            return_value=ArchivoResponse(
                id="arch-abc123",
                nombre_archivo="factura.pdf",
                tipo_mime="application/pdf",
                tamano_bytes=2048,
                url="https://fake-storage.com/factura.pdf",
                fecha_subida=datetime(2026, 4, 30, 17, 55, tzinfo=timezone.utc),
            ),
        )
        files = {"archivo": ("factura.pdf", b"%PDF content", "application/pdf")}
        response = client.post("/v1/archivos", files=files)
        assert response.status_code == 201
        assert response.json()["id"] == "arch-abc123"

    def test_subir_jpg_201(self, client, mocker):
        mocker.patch(
            "app.routes.archivos.service.subir_archivo",
            return_value=ArchivoResponse(
                id="arch-jpg001",
                nombre_archivo="dni.jpg",
                tipo_mime="image/jpeg",
                tamano_bytes=1024,
                url="https://fake-storage.com/dni.jpg",
                fecha_subida=datetime(2026, 4, 30, 17, 55, tzinfo=timezone.utc),
            ),
        )
        files = {"archivo": ("dni.jpg", b"\xff\xd8\xff", "image/jpeg")}
        response = client.post("/v1/archivos", files=files)
        assert response.status_code == 201

    def test_subir_tipo_no_permitido_415(self, client, mocker):
        from fastapi import HTTPException

        mocker.patch(
            "app.routes.archivos.service.subir_archivo",
            side_effect=HTTPException(
                status_code=415, detail="Tipo no permitido"
            ),
        )
        files = {"archivo": ("archivo.gif", b"GIF", "image/gif")}
        response = client.post("/v1/archivos", files=files)
        assert response.status_code == 415

    def test_subir_muy_grande_413(self, client, mocker):
        from fastapi import HTTPException

        mocker.patch(
            "app.routes.archivos.service.subir_archivo",
            side_effect=HTTPException(
                status_code=413, detail="Archivo demasiado grande"
            ),
        )
        files = {"archivo": ("grande.pdf", b"x" * 100, "application/pdf")}
        response = client.post("/v1/archivos", files=files)
        assert response.status_code == 413
