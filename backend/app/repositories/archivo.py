from sqlalchemy.orm import Session

from app.models.archivo import Archivo


class ArchivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, archivo: Archivo) -> Archivo:
        self.db.add(archivo)
        self.db.commit()
        self.db.refresh(archivo)
        return archivo

    def obtener(self, archivo_id: str) -> Archivo | None:
        return self.db.query(Archivo).filter(Archivo.id == archivo_id).first()

    def existen(self, archivo_ids: list[str]) -> bool:
        count = (
            self.db.query(Archivo).filter(Archivo.id.in_(archivo_ids)).count()
        )
        return count == len(archivo_ids)
