export type TipoTramite = "ALTA" | "BAJA"
export type EstadoTramite = "PENDIENTE" | "APROBADO" | "RECHAZADO"

export interface LoginRequest {
  usuario: string
  clave: string
}

export interface LoginResponse {
  token: string
  tipo: string
  "expira-en": number
}

export interface ArchivoResponse {
  id: string
  "nombre-archivo": string
  "tipo-mime": string
  "tamano-bytes": number
  url: string
  "fecha-subida": string
}

export interface ArchivoEnTramite {
  id: string
  nombre: string
  url: string
}

export interface TramiteRequest {
  tipo: TipoTramite
  nombre: string
  apellido: string
  dni: string
  mail: string
  telefono: string
  direccion: string
  archivo_id_1: string
  archivo_id_2: string
}

export interface TramiteCreadoResponse {
  id: string
  tipo: TipoTramite
  estado: EstadoTramite
  mensaje?: string
}

export interface TramitePublicoResponse {
  id: string
  tipo: TipoTramite
  estado: EstadoTramite
  "fecha-creacion": string
  "detalle-estado": string
  "motivo-rechazo"?: string | null
}

export interface TramiteAdminResponse {
  id: string
  tipo: TipoTramite
  estado: EstadoTramite
  nombre: string
  apellido: string
  dni: string
  mail: string
  telefono: string
  direccion: string
  "fecha-creacion": string
  "fecha-resolucion"?: string | null
  "motivo-rechazo"?: string | null
  "nota-interna"?: string | null
  "resuelto-por"?: string | null
  archivos?: ArchivoEnTramite[]
}

export interface ActualizarEstadoRequest {
  estado: EstadoTramite
  "motivo-rechazo"?: string | null
  "nota-interna"?: string | null
}

export interface ListarTramitesParams {
  estado?: EstadoTramite
  tipo?: TipoTramite
  orden?: string
  page?: number
  limit?: number
}
