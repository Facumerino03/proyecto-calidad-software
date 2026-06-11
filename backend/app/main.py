from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import archivos, auth, tramites


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Gestión de Trámites de Servicio",
    version="2.0.0",
    description="API RESTful para gestionar solicitudes de alta y baja de un servicio.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


app.include_router(auth.router, prefix="/v1")
app.include_router(tramites.router, prefix="/v1")
app.include_router(archivos.router, prefix="/v1")
