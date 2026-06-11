from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.enums import EstadoTramite, TipoTramite


class Tramite(Base):
    __tablename__ = "tramites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tracking_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    tipo: Mapped[TipoTramite] = mapped_column(
        Enum(TipoTramite, native_enum=False, length=20)
    )
    estado: Mapped[EstadoTramite] = mapped_column(
        Enum(EstadoTramite, native_enum=False, length=20),
        default=EstadoTramite.PENDIENTE,
    )
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    dni: Mapped[str] = mapped_column(String(20))
    mail: Mapped[str] = mapped_column(String(255))
    telefono: Mapped[str] = mapped_column(String(30))
    direccion: Mapped[str] = mapped_column(String(500))
    archivo_id_1: Mapped[str] = mapped_column(String(50))
    archivo_id_2: Mapped[str] = mapped_column(String(50))
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    fecha_resolucion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    motivo_rechazo: Mapped[str | None] = mapped_column(Text, nullable=True)
    nota_interna: Mapped[str | None] = mapped_column(Text, nullable=True)
    resuelto_por: Mapped[str | None] = mapped_column(String(100), nullable=True)
