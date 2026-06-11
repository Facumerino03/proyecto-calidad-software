from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Archivo(Base):
    __tablename__ = "archivos"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    nombre_archivo: Mapped[str] = mapped_column(String(255))
    tipo_mime: Mapped[str] = mapped_column(String(100))
    tamano_bytes: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(String(500))
    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
