import { api } from "./client"
import type { ArchivoResponse } from "@/types/api"

export async function subirArchivo(file: File): Promise<ArchivoResponse> {
  const formData = new FormData()
  formData.append("archivo", file)
  const response = await api.post<ArchivoResponse>("/archivos", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  })
  return response.data
}
