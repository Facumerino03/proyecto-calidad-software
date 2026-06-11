# Frontend — Trámites ISP

SPA en React + Vite + TypeScript + shadcn/ui.

## Requisitos

- Node.js 20+
- Backend corriendo en `http://localhost:8000`

## Instalación

```bash
cd frontend
npm install
```

## Desarrollo

```bash
npm run dev
```

Abre `http://localhost:5173`. El proxy de Vite redirige `/v1` al backend.

## Rutas

| Ruta | Descripción |
|------|-------------|
| `/` | Formulario público de alta/baja |
| `/consulta` | Consulta de estado por tracking ID |
| `/admin/login` | Login administrador |
| `/admin` | Panel de gestión (requiere JWT) |

## Build

```bash
npm run build
npm run preview
```
