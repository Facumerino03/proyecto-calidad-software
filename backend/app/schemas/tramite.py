from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import EstadoTramite, TipoTramite


class TramiteRequest(BaseModel):
    tipo: TipoTramite
    nombre: str
    apellido: str
    dni: str
    mail: EmailStr
    telefono: str
    direccion: str
    archivo_id_1: str
    archivo_id_2: str


class TramiteCreadoResponse(BaseModel):
    id: str
    tipo: TipoTramite
    estado: EstadoTramite
    mensaje: str = (
        "Su trámite fue registrado. Recibirá un mail con su ID de seguimiento."
    )


class ArchivoEnTramite(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre: str
    url: str


class TramitePublicoResponse(BaseModel):
    id: str
    tipo: TipoTramite
    estado: EstadoTramite
    fecha_creacion: datetime = Field(serialization_alias="fecha-creacion")
    detalle_estado: str = Field(serialization_alias="detalle-estado")
    motivo_rechazo: str | None = Field(
        default=None, serialization_alias="motivo-rechazo"
    )

    model_config = ConfigDict(populate_by_name=True)


class TramiteAdminResponse(BaseModel):
    id: str
    tipo: TipoTramite
    estado: EstadoTramite
    nombre: str
    apellido: str
    dni: str
    mail: EmailStr
    telefono: str
    direccion: str
    fecha_creacion: datetime = Field(serialization_alias="fecha-creacion")
    fecha_resolucion: datetime | None = Field(
        default=None, serialization_alias="fecha-resolucion"
    )
    motivo_rechazo: str | None = Field(
        default=None, serialization_alias="motivo-rechazo"
    )
    nota_interna: str | None = Field(
        default=None, serialization_alias="nota-interna"
    )
    resuelto_por: str | None = Field(
        default=None, serialization_alias="resuelto-por"
    )
    archivos: list[ArchivoEnTramite] = []

    model_config = ConfigDict(populate_by_name=True)


class ActualizarEstadoRequest(BaseModel):
    estado: EstadoTramite
    motivo_rechazo: str | None = Field(
        default=None, validation_alias="motivo-rechazo"
    )
    nota_interna: str | None = Field(
        default=None, validation_alias="nota-interna"
    )

    model_config = ConfigDict(populate_by_name=True)


class LoginRequest(BaseModel):
    usuario: str
    clave: str


class LoginResponse(BaseModel):
    token: str
    tipo: str = "Bearer"
    expira_en: int = Field(serialization_alias="expira-en")

    model_config = ConfigDict(populate_by_name=True)
