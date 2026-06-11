import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.archivo import Archivo
from app.repositories.archivo import ArchivoRepository
from app.schemas.archivo import ArchivoResponse
from app.storage.base import StorageBase

MIME_PERMITIDOS = {"image/jpeg", "image/png", "application/pdf"}
MAX_SIZE_BYTES = 10 * 1024 * 1024


def subir_archivo(
    file_tuple: tuple[str, bytes, str],
    storage: StorageBase,
    repo: ArchivoRepository,
) -> ArchivoResponse:
    filename, content, content_type = file_tuple

    if content_type not in MIME_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Tipo de archivo no permitido",
        )

    if len(content) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Archivo demasiado grande (máx. 10 MB)",
        )

    url = storage.upload_file(content, filename, content_type)
    archivo_id = f"arch-{uuid.uuid4().hex[:12]}"

    archivo = Archivo(
        id=archivo_id,
        nombre_archivo=filename,
        tipo_mime=content_type,
        tamano_bytes=len(content),
        url=url,
        fecha_subida=datetime.now(timezone.utc),
    )
    repo.crear(archivo)

    return ArchivoResponse(
        id=archivo.id,
        nombre_archivo=archivo.nombre_archivo,
        tipo_mime=archivo.tipo_mime,
        tamano_bytes=archivo.tamano_bytes,
        url=archivo.url,
        fecha_subida=archivo.fecha_subida,
    )
