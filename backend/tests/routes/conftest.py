import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.auth.jwt import crear_token

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def client(db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_headers():
    token, _ = crear_token("admin01")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_tramite_creado():
    return {
        "id": "TRK-2026-0001",
        "tipo": "ALTA",
        "estado": "PENDIENTE",
        "mensaje": "Su trámite fue registrado. Recibirá un mail con su ID de seguimiento.",
    }


@pytest.fixture
def mock_tramite_publico():
    return {
        "id": "TRK-2026-0001",
        "tipo": "ALTA",
        "estado": "PENDIENTE",
        "fecha-creacion": "2026-04-30T18:00:00Z",
        "detalle-estado": "En revisión por el administrador",
        "motivo-rechazo": None,
    }


@pytest.fixture
def mock_tramite_admin():
    return {
        "id": "TRK-2026-0001",
        "tipo": "ALTA",
        "estado": "PENDIENTE",
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "35712345",
        "mail": "juan.perez@email.com",
        "telefono": "2615001234",
        "direccion": "Av. Libertad 1200, San Rafael",
        "fecha-creacion": "2026-04-30T18:00:00Z",
        "fecha-resolucion": None,
        "motivo-rechazo": None,
        "nota-interna": None,
        "resuelto-por": None,
        "archivos": [],
    }


@pytest.fixture
def mock_archivo_response():
    return {
        "id": "arch-abc123",
        "nombre-archivo": "dni.pdf",
        "tipo-mime": "application/pdf",
        "tamano-bytes": 1024,
        "url": "https://fake-storage.com/dni.pdf",
        "fecha-subida": "2026-04-30T17:55:00Z",
    }
