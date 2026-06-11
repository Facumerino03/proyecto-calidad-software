import pytest

from app.models.enums import EstadoTramite, TipoTramite


@pytest.fixture
def valid_tramite_request():
    return {
        "tipo": "ALTA",
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "35712345",
        "mail": "juan.perez@email.com",
        "telefono": "2615001234",
        "direccion": "Av. Libertad 1200, San Rafael",
        "archivo_id_1": "arch-abc123",
        "archivo_id_2": "arch-def456",
    }


@pytest.fixture
def valid_tramite_request_baja():
    return {
        "tipo": "BAJA",
        "nombre": "María",
        "apellido": "González",
        "dni": "28904321",
        "mail": "maria.gonzalez@email.com",
        "telefono": "2604998877",
        "direccion": "Calle Italia 450, San Rafael",
        "archivo_id_1": "arch-abc123",
        "archivo_id_2": "arch-def456",
    }


@pytest.fixture
def actualizar_aprobado():
    return {"estado": "APROBADO"}


@pytest.fixture
def actualizar_rechazado():
    return {
        "estado": "RECHAZADO",
        "motivo-rechazo": "La documentación adjunta está ilegible.",
    }


@pytest.fixture
def actualizar_rechazado_sin_motivo():
    return {"estado": "RECHAZADO"}
