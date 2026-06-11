class TestAuthRoutes:

    def test_login_exitoso_200(self, client):
        response = client.post(
            "/v1/admin/login",
            json={"usuario": "admin01", "clave": "Secreta123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["tipo"] == "Bearer"
        assert data["expira-en"] == 3600

    def test_login_credenciales_invalidas_401(self, client):
        response = client.post(
            "/v1/admin/login",
            json={"usuario": "admin01", "clave": "incorrecta"},
        )
        assert response.status_code == 401

    def test_login_datos_faltantes_422(self, client):
        response = client.post("/v1/admin/login", json={"usuario": "admin01"})
        assert response.status_code == 422
