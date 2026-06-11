from enum import Enum


class TipoTramite(str, Enum):
    ALTA = "ALTA"
    BAJA = "BAJA"


class EstadoTramite(str, Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
