# Backend — Gestión de Trámites ISP

API REST en FastAPI según el contrato OpenAPI del proyecto. Persistencia en **PostgreSQL** con migraciones **Alembic**.

## Estructura (MVC + capas)

- `app/models/` — entidades SQLAlchemy
- `app/schemas/` — DTOs Pydantic (request/response)
- `app/repositories/` — acceso a datos
- `app/services/` — lógica de negocio
- `app/routes/` — controladores HTTP
- `alembic/` — migraciones de base de datos
- `tests/` — tests unitarios (SQLite en memoria; no requieren Postgres)

---

## Guía paso a paso (primera vez)

### 1. Requisitos

- [uv](https://docs.astral.sh/uv/) (gestor de dependencias y entornos)
- Python 3.12 (uv lo instala automáticamente si falta; ver `.python-version`)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (recomendado) **o** PostgreSQL instalado localmente

Instalar uv (si no lo tenés):

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Levantar PostgreSQL con Docker (opción recomendada)

Desde la carpeta `backend/`:

```bash
docker compose up -d
```

Esto crea:

| Parámetro | Valor |
|-----------|-------|
| Usuario   | `tramites` |
| Clave     | `tramites` |
| Base      | `tramites_db` |
| Puerto    | `5432` |

Verificá que esté listo:

```bash
docker compose ps
```

Debería mostrar `healthy` en el servicio `postgres`.

### 2b. Alternativa: PostgreSQL instalado a mano

Si no usás Docker, creá la base en `psql` o pgAdmin:

```sql
CREATE USER tramites WITH PASSWORD 'tramites';
CREATE DATABASE tramites_db OWNER tramites;
GRANT ALL PRIVILEGES ON DATABASE tramites_db TO tramites;
```

Ajustá `DATABASE_URL` en `.env` con tu usuario, clave, host y puerto.

### 3. Entorno Python (con uv)

```bash
cd backend
uv sync
```

`uv sync` crea `.venv`, instala dependencias desde `uv.lock` (incluye grupo `dev` con pytest) y deja el proyecto listo.

Comandos útiles:

| Comando | Qué hace |
|---------|----------|
| `uv sync` | Instala/actualiza dependencias según `uv.lock` |
| `uv lock` | Regenera `uv.lock` tras cambiar `pyproject.toml` |
| `uv add <paquete>` | Agrega dependencia de producción |
| `uv add --group dev <paquete>` | Agrega dependencia de desarrollo |
| `uv run <comando>` | Ejecuta un comando dentro del venv (sin activar) |

Alternativa con pip (sin uv):

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[test]"
```

### 4. Variables de entorno

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux / macOS
```

El `.env` por defecto apunta a Docker:

```env
DATABASE_URL=postgresql+psycopg://tramites:tramites@localhost:5432/tramites_db
```

### 5. Aplicar migraciones (crear tablas)

Con Postgres corriendo:

```bash
uv run alembic upgrade head
```

Esto ejecuta la migración inicial (`001_initial_schema`) y crea las tablas `archivos` y `tramites`.

Comandos útiles de Alembic:

| Comando | Qué hace |
|---------|----------|
| `alembic current` | Muestra la revisión aplicada |
| `alembic history` | Lista todas las migraciones |
| `alembic downgrade -1` | Revierte la última migración |
| `alembic upgrade head` | Aplica todas las migraciones pendientes |

### 6. Correr la API

```bash
uv run uvicorn app.main:app --reload
```

Documentación interactiva: `http://localhost:8000/docs`  
Base URL de la API: `http://localhost:8000/v1`

Credenciales admin por defecto: `admin01` / `Secreta123!`

---

## Tests (no necesitan PostgreSQL)

Los tests usan SQLite en memoria. No necesitan PostgreSQL:

```bash
uv run pytest -v
```

---

## Cuando cambies los modelos (nuevas migraciones)

1. Modificá el modelo en `app/models/`.
2. Generá la migración automática:

   ```bash
   uv run alembic revision --autogenerate -m "descripcion del cambio"
   ```

3. Revisá el archivo generado en `alembic/versions/`.
4. Aplicá:

   ```bash
   uv run alembic upgrade head
   ```

---

## Endpoints principales

| Método | Ruta | Auth |
|--------|------|------|
| POST | `/v1/admin/login` | No |
| POST | `/v1/archivos` | No |
| POST | `/v1/tramites` | No |
| GET | `/v1/tramites/{id}` | Opcional (admin = vista completa) |
| GET | `/v1/tramites` | Bearer JWT |
| PATCH | `/v1/tramites/{id}` | Bearer JWT |

---

## Resolución de problemas

**`connection refused` al arrancar o migrar**  
Postgres no está corriendo. Ejecutá `docker compose up -d` o verificá que el servicio local esté activo.

**`alembic upgrade head` falla con autenticación**  
Revisá que `DATABASE_URL` en `.env` coincida con usuario/clave/base de Postgres.

**Quiero empezar de cero (borrar datos)**  

```bash
docker compose down -v    # borra volumen de Docker
docker compose up -d
uv run alembic upgrade head
```
