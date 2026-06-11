import { useState } from "react"
import { obtenerTramite } from "@/api/tramites"
import { getErrorMessage } from "@/api/client"
import { EstadoBadge } from "@/components/EstadoBadge"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { TramitePublicoResponse } from "@/types/api"

function formatFecha(fecha: string) {
  return new Date(fecha).toLocaleString("es-AR")
}

export function ConsultaPage() {
  const [trackingId, setTrackingId] = useState("")
  const [tramite, setTramite] = useState<TramitePublicoResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [cargando, setCargando] = useState(false)

  async function consultar() {
    if (!trackingId.trim()) return
    setCargando(true)
    setError(null)
    setTramite(null)
    try {
      const res = await obtenerTramite(trackingId.trim())
      if ("detalle-estado" in res) {
        setTramite(res)
      }
    } catch (e) {
      setError(getErrorMessage(e))
    } finally {
      setCargando(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Consultar estado del trámite</CardTitle>
        <CardDescription>
          Ingresá tu ID de seguimiento (ej: TRK-2026-0001)
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end">
          <div className="flex-1 space-y-2">
            <Label htmlFor="tracking-id">ID de seguimiento</Label>
            <Input
              id="tracking-id"
              placeholder="TRK-2026-0001"
              value={trackingId}
              onChange={(e) => setTrackingId(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && consultar()}
            />
          </div>
          <Button onClick={consultar} disabled={cargando}>
            {cargando ? "Consultando..." : "Consultar"}
          </Button>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertTitle>No se pudo consultar</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {tramite && (
          <div className="space-y-4 rounded-lg border p-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono font-medium">{tramite.id}</span>
              <EstadoBadge estado={tramite.estado} />
              <span className="text-sm text-muted-foreground">
                {tramite.tipo}
              </span>
            </div>
            <div className="grid gap-2 text-sm">
              <p>
                <span className="text-muted-foreground">Fecha: </span>
                {formatFecha(tramite["fecha-creacion"])}
              </p>
              <p>
                <span className="text-muted-foreground">Estado: </span>
                {tramite["detalle-estado"]}
              </p>
              {tramite["motivo-rechazo"] && (
                <Alert variant="destructive">
                  <AlertTitle>Motivo de rechazo</AlertTitle>
                  <AlertDescription>
                    {tramite["motivo-rechazo"]}
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
