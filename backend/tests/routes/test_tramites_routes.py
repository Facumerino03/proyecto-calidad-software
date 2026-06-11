class TestTramitesRoutes:

    def test_crear_tramite_201(self, client, valid_tramite_request, mocker):
        from app.schemas.tramite import TramiteCreadoResponse
        from app.models.enums import EstadoTramite, TipoTramite

        mocker.patch(
            "app.routes.tramites.service.crear_tramite",
            return_value=TramiteCreadoResponse(
                id="TRK-2026-0001",
                tipo=TipoTramite.ALTA,
                estado=EstadoTramite.PENDIENTE,
            ),
        )
        response = client.post("/v1/tramites", json=valid_tramite_request)
        assert response.status_code == 201

    def test_crear_tramite_422(self, client):
        response = client.post("/v1/tramites", json={"tipo": "ALTA"})
        assert response.status_code == 422

    def test_obtener_tramite_publico_200(
        self, client, mock_tramite_publico, mocker
    ):
        from app.schemas.tramite import TramitePublicoResponse
        from app.models.enums import EstadoTramite, TipoTramite
        from datetime import datetime, timezone

        mocker.patch(
            "app.routes.tramites.service.obtener_tramite",
            return_value=TramitePublicoResponse(
                id="TRK-2026-0001",
                tipo=TipoTramite.ALTA,
                estado=EstadoTramite.PENDIENTE,
                fecha_creacion=datetime(2026, 4, 30, 18, 0, tzinfo=timezone.utc),
                detalle_estado="En revisión por el administrador",
            ),
        )
        response = client.get("/v1/tramites/TRK-2026-0001")
        assert response.status_code == 200
        assert response.json()["id"] == "TRK-2026-0001"
        assert "dni" not in response.json()

    def test_obtener_tramite_admin_200(
        self, client, admin_headers, mock_tramite_admin, mocker
    ):
        from app.schemas.tramite import TramiteAdminResponse
        from app.models.enums import EstadoTramite, TipoTramite
        from datetime import datetime, timezone

        mocker.patch(
            "app.routes.tramites.service.obtener_tramite",
            return_value=TramiteAdminResponse(
                id="TRK-2026-0001",
                tipo=TipoTramite.ALTA,
                estado=EstadoTramite.PENDIENTE,
                nombre="Juan",
                apellido="Pérez",
                dni="35712345",
                mail="juan.perez@email.com",
                telefono="2615001234",
                direccion="Av. Libertad 1200, San Rafael",
                fecha_creacion=datetime(2026, 4, 30, 18, 0, tzinfo=timezone.utc),
            ),
        )
        response = client.get(
            "/v1/tramites/TRK-2026-0001", headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["dni"] == "35712345"

    def test_obtener_tramite_no_existe_404(self, client, mocker):
        from fastapi import HTTPException

        mocker.patch(
            "app.routes.tramites.service.obtener_tramite",
            side_effect=HTTPException(status_code=404, detail="No existe"),
        )
        response = client.get("/v1/tramites/TRK-2026-9999")
        assert response.status_code == 404

    def test_listar_tramites_200(self, client, admin_headers, mocker):
        mocker.patch("app.routes.tramites.service.listar_tramites", return_value=[])
        response = client.get("/v1/tramites", headers=admin_headers)
        assert response.status_code == 200

    def test_listar_tramites_sin_auth_401(self, client):
        response = client.get("/v1/tramites")
        assert response.status_code == 401

    def test_listar_tramites_filtro_estado(self, client, admin_headers, mocker):
        mocker.patch("app.routes.tramites.service.listar_tramites", return_value=[])
        response = client.get(
            "/v1/tramites?estado=PENDIENTE", headers=admin_headers
        )
        assert response.status_code == 200

    def test_actualizar_estado_aprobado_200(self, client, admin_headers, mocker):
        from app.schemas.tramite import TramiteAdminResponse
        from app.models.enums import EstadoTramite, TipoTramite
        from datetime import datetime, timezone

        admin_response = TramiteAdminResponse(
            id="TRK-2026-0001",
            tipo=TipoTramite.ALTA,
            estado=EstadoTramite.APROBADO,
            nombre="Juan",
            apellido="Pérez",
            dni="35712345",
            mail="juan.perez@email.com",
            telefono="2615001234",
            direccion="Av. Libertad 1200",
            fecha_creacion=datetime(2026, 4, 30, 18, 0, tzinfo=timezone.utc),
            fecha_resolucion=datetime(2026, 4, 30, 20, 30, tzinfo=timezone.utc),
            resuelto_por="admin01",
        )
        mocker.patch("app.routes.tramites.service.actualizar_estado")
        mocker.patch(
            "app.routes.tramites.service.obtener_tramite",
            return_value=admin_response,
        )
        response = client.patch(
            "/v1/tramites/TRK-2026-0001",
            json={"estado": "APROBADO"},
            headers=admin_headers,
        )
        assert response.status_code == 200
        assert response.json()["estado"] == "APROBADO"

    def test_actualizar_estado_rechazado_200(self, client, admin_headers, mocker):
        from app.schemas.tramite import TramiteAdminResponse
        from app.models.enums import EstadoTramite, TipoTramite
        from datetime import datetime, timezone

        admin_response = TramiteAdminResponse(
            id="TRK-2026-0001",
            tipo=TipoTramite.ALTA,
            estado=EstadoTramite.RECHAZADO,
            nombre="Juan",
            apellido="Pérez",
            dni="35712345",
            mail="juan.perez@email.com",
            telefono="2615001234",
            direccion="Av. Libertad 1200",
            fecha_creacion=datetime(2026, 4, 30, 18, 0, tzinfo=timezone.utc),
            motivo_rechazo="Documentación ilegible.",
        )
        mocker.patch("app.routes.tramites.service.actualizar_estado")
        mocker.patch(
            "app.routes.tramites.service.obtener_tramite",
            return_value=admin_response,
        )
        response = client.patch(
            "/v1/tramites/TRK-2026-0001",
            json={
                "estado": "RECHAZADO",
                "motivo-rechazo": "Documentación ilegible.",
            },
            headers=admin_headers,
        )
        assert response.status_code == 200
        assert response.json()["estado"] == "RECHAZADO"

    def test_actualizar_rechazado_sin_motivo_400(
        self, client, admin_headers, mocker
    ):
        from fastapi import HTTPException

        mocker.patch(
            "app.routes.tramites.service.actualizar_estado",
            side_effect=HTTPException(status_code=400, detail="Falta motivo"),
        )
        response = client.patch(
            "/v1/tramites/TRK-2026-0001",
            json={"estado": "RECHAZADO"},
            headers=admin_headers,
        )
        assert response.status_code == 400

    def test_actualizar_sin_auth_401(self, client):
        response = client.patch(
            "/v1/tramites/TRK-2026-0001",
            json={"estado": "APROBADO"},
        )
        assert response.status_code == 401
