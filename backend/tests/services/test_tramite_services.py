from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import EstadoTramite, TipoTramite
from app.services import tramite as service
from app.services.email import EmailService


class TestTramiteServices:

    def test_crear_tramite(
        self, tramite_repo, archivo_repo, archivos_en_db, valid_tramite_data
    ):
        email_svc = EmailService()
        result = service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        assert result.estado == EstadoTramite.PENDIENTE
        assert result.id.startswith("TRK-")

    def test_crear_tramite_envia_mail(
        self, tramite_repo, archivo_repo, archivos_en_db, valid_tramite_data, mocker
    ):
        email_svc = MagicMock(spec=EmailService)
        service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        email_svc.enviar_id_seguimiento.assert_called_once()

    def test_crear_tramite_archivos_inexistentes(
        self, tramite_repo, archivo_repo, valid_tramite_data
    ):
        email_svc = EmailService()
        with pytest.raises(HTTPException) as exc:
            service.crear_tramite(
                valid_tramite_data, tramite_repo, archivo_repo, email_svc
            )
        assert exc.value.status_code == 422

    def test_obtener_tramite_publico(
        self, tramite_repo, archivo_repo, archivos_en_db, valid_tramite_data
    ):
        email_svc = EmailService()
        creado = service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        result = service.obtener_tramite(
            creado.id, tramite_repo, archivo_repo, es_admin=False
        )
        assert result.id == creado.id
        assert not hasattr(result, "dni") or getattr(result, "dni", None) is None

    def test_obtener_tramite_admin(
        self, tramite_repo, archivo_repo, archivos_en_db, valid_tramite_data
    ):
        email_svc = EmailService()
        creado = service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        result = service.obtener_tramite(
            creado.id, tramite_repo, archivo_repo, es_admin=True
        )
        assert result.dni == valid_tramite_data.dni
        assert result.mail == valid_tramite_data.mail

    def test_obtener_tramite_no_existe(self, tramite_repo, archivo_repo):
        with pytest.raises(HTTPException) as exc:
            service.obtener_tramite(
                "TRK-2026-9999", tramite_repo, archivo_repo, es_admin=False
            )
        assert exc.value.status_code == 404

    def test_listar_tramites_sin_filtros(
        self,
        tramite_repo,
        archivo_repo,
        archivos_en_db,
        valid_tramite_data,
        valid_tramite_request_baja,
    ):
        from app.schemas.tramite import TramiteRequest

        email_svc = EmailService()
        service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        baja = TramiteRequest(**valid_tramite_request_baja)
        baja.mail = "otro@email.com"
        service.crear_tramite(baja, tramite_repo, archivo_repo, email_svc)

        result = service.listar_tramites(tramite_repo)
        assert len(result) == 2

    def test_listar_tramites_filtro_estado(
        self, tramite_repo, archivo_repo, archivos_en_db, valid_tramite_data, aprobar_data
    ):
        email_svc = EmailService()
        creado = service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        service.actualizar_estado(
            creado.id,
            aprobar_data,
            tramite_repo,
            email_svc,
            admin_usuario="admin01",
        )

        pendientes = service.listar_tramites(
            tramite_repo, estado=EstadoTramite.PENDIENTE
        )
        assert len(pendientes) == 0

        aprobados = service.listar_tramites(
            tramite_repo, estado=EstadoTramite.APROBADO
        )
        assert len(aprobados) == 1

    def test_listar_tramites_filtro_tipo(
        self,
        tramite_repo,
        archivo_repo,
        archivos_en_db,
        valid_tramite_data,
        valid_tramite_request_baja,
    ):
        from app.schemas.tramite import TramiteRequest

        email_svc = EmailService()
        service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        baja = TramiteRequest(**valid_tramite_request_baja)
        baja.mail = "otro@email.com"
        service.crear_tramite(baja, tramite_repo, archivo_repo, email_svc)

        altas = service.listar_tramites(tramite_repo, tipo=TipoTramite.ALTA)
        assert len(altas) == 1
        assert altas[0].tipo == TipoTramite.ALTA

    def test_actualizar_aprobado(
        self, tramite_repo, archivo_repo, archivos_en_db, valid_tramite_data, aprobar_data
    ):
        email_svc = EmailService()
        creado = service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        result = service.actualizar_estado(
            creado.id,
            aprobar_data,
            tramite_repo,
            email_svc,
            admin_usuario="admin01",
        )
        assert result.estado == EstadoTramite.APROBADO
        assert result.fecha_resolucion is not None
        assert result.resuelto_por == "admin01"

    def test_actualizar_rechazado(
        self, tramite_repo, archivo_repo, archivos_en_db, valid_tramite_data, rechazar_data
    ):
        email_svc = EmailService()
        creado = service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        result = service.actualizar_estado(
            creado.id,
            rechazar_data,
            tramite_repo,
            email_svc,
            admin_usuario="admin01",
        )
        assert result.estado == EstadoTramite.RECHAZADO
        assert result.motivo_rechazo == rechazar_data.motivo_rechazo

    def test_actualizar_rechazado_sin_motivo(
        self,
        tramite_repo,
        archivo_repo,
        archivos_en_db,
        valid_tramite_data,
        rechazar_sin_motivo_data,
    ):
        email_svc = EmailService()
        creado = service.crear_tramite(
            valid_tramite_data, tramite_repo, archivo_repo, email_svc
        )
        with pytest.raises(HTTPException) as exc:
            service.actualizar_estado(
                creado.id,
                rechazar_sin_motivo_data,
                tramite_repo,
                email_svc,
                admin_usuario="admin01",
            )
        assert exc.value.status_code == 400

    def test_actualizar_estado_no_encontrado(self, tramite_repo, aprobar_data):
        email_svc = EmailService()
        with pytest.raises(HTTPException) as exc:
            service.actualizar_estado(
                "TRK-2026-9999",
                aprobar_data,
                tramite_repo,
                email_svc,
                admin_usuario="admin01",
            )
        assert exc.value.status_code == 404
