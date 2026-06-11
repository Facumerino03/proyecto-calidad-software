import { api } from "./client"
import type { LoginRequest, LoginResponse } from "@/types/api"

export async function login(data: LoginRequest): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>("/admin/login", data)
  return response.data
}
