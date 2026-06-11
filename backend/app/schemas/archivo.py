from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ArchivoResponse(BaseModel):
    id: str
    nombre_archivo: str = Field(serialization_alias="nombre-archivo")
    tipo_mime: str = Field(serialization_alias="tipo-mime")
    tamano_bytes: int = Field(serialization_alias="tamano-bytes")
    url: str
    fecha_subida: datetime = Field(serialization_alias="fecha-subida")

    model_config = ConfigDict(populate_by_name=True)
