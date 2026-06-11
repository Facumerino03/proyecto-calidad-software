from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_admin, get_current_admin_optional
from app.database import get_db
from app.models.enums import EstadoTramite, TipoTramite
from app.repositories.archivo import ArchivoRepository
from app.repositories.tramite import TramiteRepository
from app.schemas.tramite import (
    ActualizarEstadoRequest,
    TramiteAdminResponse,
    TramiteCreadoResponse,
    TramitePublicoResponse,
    TramiteRequest,
)
from app.services import tramite as service
from app.services.email import EmailService

router = APIRouter(tags=["Trámites"], prefix="/tramites")

_email_service = EmailService()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[TramiteAdminResponse],
    response_model_by_alias=True,
)
def listar_tramites(
    estado: EstadoTramite | None = None,
    tipo: TipoTramite | None = None,
    orden: str = "desc",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    _admin: str = Depends(get_current_admin),
) -> list[TramiteAdminResponse]:
    repo = TramiteRepository(db)
    archivo_repo = ArchivoRepository(db)
    tramites = service.listar_tramites(
        repo, estado=estado, tipo=tipo, orden=orden, page=page, limit=limit
    )
    return [
        service.obtener_tramite(t.tracking_id, repo, archivo_repo, es_admin=True)
        for t in tramites
    ]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TramiteCreadoResponse,
    response_model_by_alias=True,
)
def crear_tramite(
    body: TramiteRequest,
    db: Session = Depends(get_db),
) -> TramiteCreadoResponse:
    repo = TramiteRepository(db)
    archivo_repo = ArchivoRepository(db)
    return service.crear_tramite(body, repo, archivo_repo, _email_service)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=True,
)
def obtener_tramite(
    id: str,
    db: Session = Depends(get_db),
    admin: str | None = Depends(get_current_admin_optional),
) -> TramitePublicoResponse | TramiteAdminResponse:
    repo = TramiteRepository(db)
    archivo_repo = ArchivoRepository(db)
    return service.obtener_tramite(id, repo, archivo_repo, es_admin=admin is not None)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=TramiteAdminResponse,
    response_model_by_alias=True,
)
def actualizar_estado_tramite(
    id: str,
    body: ActualizarEstadoRequest,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
) -> TramiteAdminResponse:
    repo = TramiteRepository(db)
    archivo_repo = ArchivoRepository(db)
    service.actualizar_estado(
        id, body, repo, _email_service, admin_usuario=admin
    )
    return service.obtener_tramite(id, repo, archivo_repo, es_admin=True)
