import { useCallback, useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { actualizarEstado, listarTramites } from "@/api/tramites"
import { getErrorMessage } from "@/api/client"
import { useAuth } from "@/hooks/useAuth"
import { EstadoBadge } from "@/components/EstadoBadge"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Textarea } from "@/components/ui/textarea"
import type {
  EstadoTramite,
  TipoTramite,
  TramiteAdminResponse,
} from "@/types/api"

function formatFecha(fecha: string) {
  return new Date(fecha).toLocaleString("es-AR")
}

export function AdminPage() {
  const navigate = useNavigate()
  const { logout } = useAuth()
  const [tramites, setTramites] = useState<TramiteAdminResponse[]>([])
  const [filtroEstado, setFiltroEstado] = useState<string>("todos")
  const [filtroTipo, setFiltroTipo] = useState<string>("todos")
  const [seleccionado, setSeleccionado] = useState<TramiteAdminResponse | null>(
    null
  )
  const [motivoRechazo, setMotivoRechazo] = useState("")
  const [notaInterna, setNotaInterna] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [cargando, setCargando] = useState(false)
  const [accionando, setAccionando] = useState(false)

  const cargar = useCallback(async () => {
    setCargando(true)
    setError(null)
    try {
      const params: { estado?: EstadoTramite; tipo?: TipoTramite } = {}
      if (filtroEstado !== "todos")
        params.estado = filtroEstado as EstadoTramite
      if (filtroTipo !== "todos") params.tipo = filtroTipo as TipoTramite
      const data = await listarTramites(params)
      setTramites(data)
    } catch (e) {
      setError(getErrorMessage(e))
    } finally {
      setCargando(false)
    }
  }, [filtroEstado, filtroTipo])

  useEffect(() => {
    cargar()
  }, [cargar])

  function handleLogout() {
    logout()
    navigate("/admin/login")
  }

  async function cambiarEstado(
    estado: EstadoTramite,
    extra?: { "motivo-rechazo"?: string; "nota-interna"?: string }
  ) {
    if (!seleccionado) return
    if (estado === "RECHAZADO" && !motivoRechazo.trim()) {
      setError("El motivo de rechazo es obligatorio.")
      return
    }
    setAccionando(true)
    setError(null)
    try {
      const actualizado = await actualizarEstado(seleccionado.id, {
        estado,
        "motivo-rechazo": estado === "RECHAZADO" ? motivoRechazo : undefined,
        "nota-interna": extra?.["nota-interna"] ?? (notaInterna || undefined),
      })
      setSeleccionado(actualizado)
      setMotivoRechazo("")
      await cargar()
    } catch (e) {
      setError(getErrorMessage(e))
    } finally {
      setAccionando(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Panel administrativo</h1>
          <p className="text-sm text-muted-foreground">
            Gestión de trámites de alta y baja
          </p>
        </div>
        <Button variant="outline" onClick={handleLogout}>
          Cerrar sesión
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="flex flex-wrap items-end gap-4">
        <div className="w-40 space-y-1">
          <p className="text-sm font-medium">Estado</p>
          <Select value={filtroEstado} onValueChange={setFiltroEstado}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="todos">Todos</SelectItem>
              <SelectItem value="PENDIENTE">Pendiente</SelectItem>
              <SelectItem value="APROBADO">Aprobado</SelectItem>
              <SelectItem value="RECHAZADO">Rechazado</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="w-40 space-y-1">
          <p className="text-sm font-medium">Tipo</p>
          <Select value={filtroTipo} onValueChange={setFiltroTipo}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="todos">Todos</SelectItem>
              <SelectItem value="ALTA">Alta</SelectItem>
              <SelectItem value="BAJA">Baja</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <Button onClick={cargar} disabled={cargando}>
          {cargando ? "Actualizando..." : "Actualizar"}
        </Button>
      </div>

      <div className="rounded-lg border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead>Solicitante</TableHead>
              <TableHead>DNI</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead>Fecha</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tramites.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-muted-foreground">
                  {cargando ? "Cargando..." : "No hay trámites"}
                </TableCell>
              </TableRow>
            ) : (
              tramites.map((t) => (
                <TableRow
                  key={t.id}
                  className="cursor-pointer"
                  onClick={() => {
                    setSeleccionado(t)
                    setMotivoRechazo("")
                    setNotaInterna(t["nota-interna"] ?? "")
                    setError(null)
                  }}
                >
                  <TableCell className="font-mono text-xs">{t.id}</TableCell>
                  <TableCell>{t.tipo}</TableCell>
                  <TableCell>
                    {t.nombre} {t.apellido}
                  </TableCell>
                  <TableCell>{t.dni}</TableCell>
                  <TableCell>{t.mail}</TableCell>
                  <TableCell>
                    <EstadoBadge estado={t.estado} />
                  </TableCell>
                  <TableCell className="text-xs">
                    {formatFecha(t["fecha-creacion"])}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <Dialog
        open={!!seleccionado}
        onOpenChange={(open) => !open && setSeleccionado(null)}
      >
        <DialogContent className="max-h-[90vh] max-w-lg overflow-y-auto">
          {seleccionado && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <span className="font-mono">{seleccionado.id}</span>
                  <EstadoBadge estado={seleccionado.estado} />
                </DialogTitle>
                <DialogDescription>
                  {seleccionado.tipo} — {seleccionado.nombre}{" "}
                  {seleccionado.apellido}
                </DialogDescription>
              </DialogHeader>

              <div className="space-y-2 text-sm">
                <p>
                  <span className="text-muted-foreground">DNI: </span>
                  {seleccionado.dni}
                </p>
                <p>
                  <span className="text-muted-foreground">Email: </span>
                  {seleccionado.mail}
                </p>
                <p>
                  <span className="text-muted-foreground">Teléfono: </span>
                  {seleccionado.telefono}
                </p>
                <p>
                  <span className="text-muted-foreground">Dirección: </span>
                  {seleccionado.direccion}
                </p>
                <p>
                  <span className="text-muted-foreground">Creado: </span>
                  {formatFecha(seleccionado["fecha-creacion"])}
                </p>
                {seleccionado["fecha-resolucion"] && (
                  <p>
                    <span className="text-muted-foreground">Resuelto: </span>
                    {formatFecha(seleccionado["fecha-resolucion"])}
                  </p>
                )}
                {seleccionado["motivo-rechazo"] && (
                  <p>
                    <span className="text-muted-foreground">Motivo rechazo: </span>
                    {seleccionado["motivo-rechazo"]}
                  </p>
                )}
                {seleccionado["resuelto-por"] && (
                  <p>
                    <span className="text-muted-foreground">Resuelto por: </span>
                    {seleccionado["resuelto-por"]}
                  </p>
                )}
              </div>

              {seleccionado.archivos && seleccionado.archivos.length > 0 && (
                <>
                  <Separator />
                  <div className="space-y-2">
                    <p className="text-sm font-medium">Archivos adjuntos</p>
                    {seleccionado.archivos.map((a) => (
                      <a
                        key={a.id}
                        href={a.url}
                        target="_blank"
                        rel="noreferrer"
                        className="block text-sm text-primary underline"
                      >
                        {a.nombre}
                      </a>
                    ))}
                  </div>
                </>
              )}

              <Separator />

              <div className="space-y-3">
                <p className="text-sm font-medium">Acciones</p>
                <div className="flex flex-wrap gap-2">
                  <Button
                    size="sm"
                    disabled={accionando}
                    onClick={() => cambiarEstado("APROBADO")}
                  >
                    Aprobar
                  </Button>
                  <Button
                    size="sm"
                    variant="secondary"
                    disabled={accionando}
                    onClick={() =>
                      cambiarEstado("PENDIENTE", {
                        "nota-interna": notaInterna,
                      })
                    }
                  >
                    Revertir a pendiente
                  </Button>
                </div>
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">
                    Rechazar (motivo obligatorio)
                  </p>
                  <Textarea
                    placeholder="Motivo del rechazo..."
                    value={motivoRechazo}
                    onChange={(e) => setMotivoRechazo(e.target.value)}
                  />
                  <Button
                    size="sm"
                    variant="destructive"
                    disabled={accionando}
                    onClick={() => cambiarEstado("RECHAZADO")}
                  >
                    Rechazar
                  </Button>
                </div>
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">Nota interna</p>
                  <Textarea
                    placeholder="Nota interna (opcional)"
                    value={notaInterna}
                    onChange={(e) => setNotaInterna(e.target.value)}
                  />
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}
