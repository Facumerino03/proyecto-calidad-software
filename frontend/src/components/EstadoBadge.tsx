import { Badge } from "@/components/ui/badge"
import type { EstadoTramite } from "@/types/api"

const variantMap: Record<
  EstadoTramite,
  "default" | "secondary" | "outline" | "destructive"
> = {
  PENDIENTE: "outline",
  APROBADO: "default",
  RECHAZADO: "secondary",
}

export function EstadoBadge({ estado }: { estado: EstadoTramite }) {
  return <Badge variant={variantMap[estado]}>{estado}</Badge>
}
