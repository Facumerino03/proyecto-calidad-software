import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.archivo import Archivo
from app.repositories.archivo import ArchivoRepository
from app.repositories.tramite import TramiteRepository
from app.schemas.tramite import ActualizarEstadoRequest, TramiteRequest

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def tramite_repo(db):
    return TramiteRepository(db)


@pytest.fixture
def archivo_repo(db):
    return ArchivoRepository(db)


@pytest.fixture
def archivos_en_db(archivo_repo, db):
    for aid, nombre in [
        ("arch-abc123", "dni.pdf"),
        ("arch-def456", "impuesto.pdf"),
    ]:
        archivo = Archivo(
            id=aid,
            nombre_archivo=nombre,
            tipo_mime="application/pdf",
            tamano_bytes=1024,
            url=f"https://storage.test/{aid}",
        )
        archivo_repo.crear(archivo)
    return archivo_repo


@pytest.fixture
def valid_tramite_data(valid_tramite_request):
    return TramiteRequest(**valid_tramite_request)


@pytest.fixture
def aprobar_data(actualizar_aprobado):
    return ActualizarEstadoRequest(**actualizar_aprobado)


@pytest.fixture
def rechazar_data(actualizar_rechazado):
    return ActualizarEstadoRequest(**actualizar_rechazado)


@pytest.fixture
def rechazar_sin_motivo_data(actualizar_rechazado_sin_motivo):
    return ActualizarEstadoRequest(**actualizar_rechazado_sin_motivo)
