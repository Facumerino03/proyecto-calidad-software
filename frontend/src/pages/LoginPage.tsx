import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useNavigate } from "react-router-dom"
import { login } from "@/api/auth"
import { getErrorMessage } from "@/api/client"
import { useAuth } from "@/hooks/useAuth"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const loginSchema = z.object({
  usuario: z.string().min(1, "Requerido"),
  clave: z.string().min(1, "Requerido"),
})

type LoginForm = z.infer<typeof loginSchema>

export function LoginPage() {
  const navigate = useNavigate()
  const { login: saveToken } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [cargando, setCargando] = useState(false)

  const form = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { usuario: "", clave: "" },
  })

  async function onSubmit(values: LoginForm) {
    setCargando(true)
    setError(null)
    try {
      const res = await login(values)
      saveToken(res.token)
      navigate("/admin")
    } catch (e) {
      setError(getErrorMessage(e))
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="mx-auto max-w-md">
      <Card>
        <CardHeader>
          <CardTitle>Acceso administrador</CardTitle>
          <CardDescription>
            Ingresá tus credenciales para gestionar trámites.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertTitle>Error de autenticación</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="usuario"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Usuario</FormLabel>
                    <FormControl>
                      <Input {...field} autoComplete="username" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="clave"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Clave</FormLabel>
                    <FormControl>
                      <Input
                        type="password"
                        {...field}
                        autoComplete="current-password"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full" disabled={cargando}>
                {cargando ? "Ingresando..." : "Ingresar"}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  )
}
