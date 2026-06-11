import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import { Layout } from "@/components/Layout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { AdminPage } from "@/pages/AdminPage"
import { ConsultaPage } from "@/pages/ConsultaPage"
import { FormularioPage } from "@/pages/FormularioPage"
import { LoginPage } from "@/pages/LoginPage"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<FormularioPage />} />
          <Route path="consulta" element={<ConsultaPage />} />
          <Route path="admin/login" element={<LoginPage />} />
          <Route
            path="admin"
            element={
              <ProtectedRoute>
                <AdminPage />
              </ProtectedRoute>
            }
          />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
