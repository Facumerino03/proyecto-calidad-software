import { Link, Outlet } from "react-router-dom"
import { Button } from "@/components/ui/button"

export function Layout() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
          <Link to="/" className="text-lg font-semibold">
            Trámites ISP
          </Link>
          <nav className="flex items-center gap-2">
            <Button variant="ghost" asChild>
              <Link to="/">Nuevo trámite</Link>
            </Button>
            <Button variant="ghost" asChild>
              <Link to="/consulta">Consultar estado</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link to="/admin/login">Admin</Link>
            </Button>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
