import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react"
import {
  clearStoredToken,
  getStoredToken,
  setStoredToken,
} from "@/api/client"

interface AuthContextValue {
  token: string | null
  isAuthenticated: boolean
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => getStoredToken())

  const login = useCallback((newToken: string) => {
    setStoredToken(newToken)
    setToken(newToken)
  }, [])

  const logout = useCallback(() => {
    clearStoredToken()
    setToken(null)
  }, [])

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: Boolean(token),
      login,
      logout,
    }),
    [token, login, logout]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error("useAuth debe usarse dentro de AuthProvider")
  }
  return ctx
}
