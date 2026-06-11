from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.enums import EstadoTramite, TipoTramite
from app.models.tramite import Tramite
from app.repositories.archivo import ArchivoRepository
from app.repositories.tramite import TramiteRepository
from app.schemas.tramite import (
    ActualizarEstadoRequest,
    ArchivoEnTramite,
    TramiteAdminResponse,
    TramiteCreadoResponse,
    TramitePublicoResponse,
    TramiteRequest,
)
from app.services.email import EmailService

DETALLE_ESTADO = {
    EstadoTramite.PENDIENTE: "En revisión por el administrador",
    EstadoTramite.APROBADO: "Trámite aprobado",
    EstadoTramite.RECHAZADO: "Trámite rechazado",
}


def _generar_tracking_id(repo: TramiteRepository) -> str:
    year = datetime.now(timezone.utc).year
    count = repo.contar() + 1
    return f"TRK-{year}-{count:04d}"


def crear_tramite(
    data: TramiteRequest,
    repo: TramiteRepository,
    archivo_repo: ArchivoRepository,
    email_svc: EmailService,
) -> TramiteCreadoResponse:
    if not archivo_repo.existen([data.archivo_id_1, data.archivo_id_2]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Los archivos adjuntos no existen",
        )

    tracking_id = _generar_tracking_id(repo)
    tramite = repo.crear(data, tracking_id)
    email_svc.enviar_id_seguimiento(str(data.mail), tracking_id)

    return TramiteCreadoResponse(
        id=tramite.tracking_id,
        tipo=tramite.tipo,
        estado=tramite.estado,
    )


def _archivos_de_tramite(
    tramite: Tramite, archivo_repo: ArchivoRepository
) -> list[ArchivoEnTramite]:
    archivos = []
    for archivo_id in [tramite.archivo_id_1, tramite.archivo_id_2]:
        archivo = archivo_repo.obtener(archivo_id)
        if archivo:
            archivos.append(
                ArchivoEnTramite(
                    id=archivo.id,
                    nombre=archivo.nombre_archivo,
                    url=archivo.url,
                )
            )
    return archivos


def obtener_tramite(
    tracking_id: str,
    repo: TramiteRepository,
    archivo_repo: ArchivoRepository,
    es_admin: bool = False,
) -> TramitePublicoResponse | TramiteAdminResponse:
    tramite = repo.obtener(tracking_id)
    if tramite is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El recurso no existe",
        )

    if es_admin:
        return TramiteAdminResponse(
            id=tramite.tracking_id,
            tipo=tramite.tipo,
            estado=tramite.estado,
            nombre=tramite.nombre,
            apellido=tramite.apellido,
            dni=tramite.dni,
            mail=tramite.mail,
            telefono=tramite.telefono,
            direccion=tramite.direccion,
            fecha_creacion=tramite.fecha_creacion,
            fecha_resolucion=tramite.fecha_resolucion,
            motivo_rechazo=tramite.motivo_rechazo,
            nota_interna=tramite.nota_interna,
            resuelto_por=tramite.resuelto_por,
            archivos=_archivos_de_tramite(tramite, archivo_repo),
        )

    return TramitePublicoResponse(
        id=tramite.tracking_id,
        tipo=tramite.tipo,
        estado=tramite.estado,
        fecha_creacion=tramite.fecha_creacion,
        detalle_estado=DETALLE_ESTADO[tramite.estado],
        motivo_rechazo=tramite.motivo_rechazo,
    )


def listar_tramites(
    repo: TramiteRepository,
    estado: EstadoTramite | None = None,
    tipo: TipoTramite | None = None,
    orden: str = "desc",
    page: int = 1,
    limit: int = 20,
) -> list[Tramite]:
    return repo.listar(estado=estado, tipo=tipo, orden=orden, page=page, limit=limit)


def actualizar_estado(
    tracking_id: str,
    data: ActualizarEstadoRequest,
    repo: TramiteRepository,
    email_svc: EmailService,
    admin_usuario: str,
) -> Tramite:
    tramite = repo.obtener(tracking_id)
    if tramite is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El recurso no existe",
        )

    if data.estado == EstadoTramite.RECHAZADO and not data.motivo_rechazo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El campo motivo-rechazo es obligatorio al rechazar",
        )

    tramite.estado = data.estado
    tramite.motivo_rechazo = data.motivo_rechazo
    tramite.nota_interna = data.nota_interna
    tramite.resuelto_por = admin_usuario

    if data.estado in (EstadoTramite.APROBADO, EstadoTramite.RECHAZADO):
        tramite.fecha_resolucion = datetime.now(timezone.utc)
    elif data.estado == EstadoTramite.PENDIENTE:
        tramite.fecha_resolucion = None

    repo.actualizar(tramite)
    email_svc.enviar_cambio_estado(
        tramite.mail,
        tramite.tracking_id,
        data.estado.value,
        data.motivo_rechazo,
    )
    return tramite
