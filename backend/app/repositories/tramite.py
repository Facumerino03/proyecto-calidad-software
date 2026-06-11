from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.enums import EstadoTramite, TipoTramite
from app.models.tramite import Tramite
from app.schemas.tramite import TramiteRequest


class TramiteRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: TramiteRequest, tracking_id: str) -> Tramite:
        tramite = Tramite(
            tracking_id=tracking_id,
            tipo=data.tipo,
            estado=EstadoTramite.PENDIENTE,
            nombre=data.nombre,
            apellido=data.apellido,
            dni=data.dni,
            mail=str(data.mail),
            telefono=data.telefono,
            direccion=data.direccion,
            archivo_id_1=data.archivo_id_1,
            archivo_id_2=data.archivo_id_2,
        )
        self.db.add(tramite)
        self.db.commit()
        self.db.refresh(tramite)
        return tramite

    def obtener(self, tracking_id: str) -> Tramite | None:
        return (
            self.db.query(Tramite)
            .filter(Tramite.tracking_id == tracking_id)
            .first()
        )

    def listar(
        self,
        estado: EstadoTramite | None = None,
        tipo: TipoTramite | None = None,
        orden: str = "desc",
        page: int = 1,
        limit: int = 20,
    ) -> list[Tramite]:
        query = self.db.query(Tramite)
        if estado:
            query = query.filter(Tramite.estado == estado)
        if tipo:
            query = query.filter(Tramite.tipo == tipo)
        order_fn = desc if orden == "desc" else asc
        query = query.order_by(order_fn(Tramite.fecha_creacion))
        offset = (page - 1) * limit
        return query.offset(offset).limit(limit).all()

    def contar(self) -> int:
        return self.db.query(Tramite).count()

    def actualizar(self, tramite: Tramite) -> Tramite:
        self.db.commit()
        self.db.refresh(tramite)
        return tramite
