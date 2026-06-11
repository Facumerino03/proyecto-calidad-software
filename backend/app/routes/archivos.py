from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.archivo import ArchivoRepository
from app.schemas.archivo import ArchivoResponse
from app.services import archivo as service
from app.storage.local_storage import LocalStorage

router = APIRouter(tags=["Archivos"], prefix="/archivos")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ArchivoResponse,
    response_model_by_alias=True,
)
async def subir_archivo(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ArchivoResponse:
    content = await archivo.read()
    content_type = archivo.content_type or "application/octet-stream"
    file_tuple = (archivo.filename or "archivo", content, content_type)
    repo = ArchivoRepository(db)
    storage = LocalStorage()
    return service.subir_archivo(file_tuple, storage, repo)
