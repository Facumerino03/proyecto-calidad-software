import axios from "axios"

const TOKEN_KEY = "token"

export const api = axios.create({
  baseURL: "/v1",
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearStoredToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === "string") return detail
    if (Array.isArray(detail)) {
      return detail.map((d: { msg?: string }) => d.msg ?? "Error").join(", ")
    }
    return error.message
  }
  if (error instanceof Error) return error.message
  return "Ocurrió un error inesperado"
}
