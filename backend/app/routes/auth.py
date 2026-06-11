from fastapi import APIRouter, HTTPException, status

from app.config import get_settings
from app.auth.jwt import crear_token
from app.schemas.tramite import LoginRequest, LoginResponse

router = APIRouter(tags=["Tokens"])


@router.post(
    "/admin/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    response_model_by_alias=True,
)
def login_administrador(body: LoginRequest) -> LoginResponse:
    settings = get_settings()
    if body.usuario != settings.admin_user or body.clave != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o clave incorrectos",
        )
    token, expira_en = crear_token(body.usuario)
    return LoginResponse(token=token, expira_en=expira_en)
