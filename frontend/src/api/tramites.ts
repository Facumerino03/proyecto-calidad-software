import { api } from "./client"
import type {
  ActualizarEstadoRequest,
  ListarTramitesParams,
  TramiteAdminResponse,
  TramiteCreadoResponse,
  TramitePublicoResponse,
  TramiteRequest,
} from "@/types/api"

export async function crearTramite(
  data: TramiteRequest
): Promise<TramiteCreadoResponse> {
  const response = await api.post<TramiteCreadoResponse>("/tramites", data)
  return response.data
}

export async function obtenerTramite(
  id: string
): Promise<TramitePublicoResponse | TramiteAdminResponse> {
  const response = await api.get<TramitePublicoResponse | TramiteAdminResponse>(
    `/tramites/${id}`
  )
  return response.data
}

export async function listarTramites(
  params?: ListarTramitesParams
): Promise<TramiteAdminResponse[]> {
  const response = await api.get<TramiteAdminResponse[]>("/tramites", {
    params,
  })
  return response.data
}

export async function actualizarEstado(
  id: string,
  data: ActualizarEstadoRequest
): Promise<TramiteAdminResponse> {
  const response = await api.patch<TramiteAdminResponse>(
    `/tramites/${id}`,
    data
  )
  return response.data
}
