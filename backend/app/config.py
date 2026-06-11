import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str = "cambia_esto_en_produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str = (
        "postgresql+psycopg://tramites:tramites@localhost:5432/tramites_db"
    )
    admin_user: str = "admin01"
    admin_password: str = "Secreta123!"
    storage_path: str = "./uploads"
    storage_base_url: str = "http://localhost:8000/v1/archivos"


@lru_cache
def get_settings() -> Settings:
    return Settings()
