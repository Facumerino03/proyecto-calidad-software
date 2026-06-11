from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import get_settings

security = HTTPBearer(auto_error=False)


def crear_token(usuario: str) -> tuple[str, int]:
    settings = get_settings()
    expire_minutes = settings.access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {"sub": usuario, "exp": expire}
    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return token, expire_minutes * 60


def verificar_token(token: str) -> str:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        usuario: str | None = payload.get("sub")
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        return usuario
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        ) from exc


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token JWT ausente o inválido",
        )
    return verificar_token(credentials.credentials)


def get_current_admin_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str | None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        return None
    return verificar_token(credentials.credentials)
