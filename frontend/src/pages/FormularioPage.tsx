import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { subirArchivo } from "@/api/archivos"
import { crearTramite } from "@/api/tramites"
import { getErrorMessage } from "@/api/client"
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
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import type { ArchivoResponse, TipoTramite, TramiteCreadoResponse } from "@/types/api"

const formSchema = z.object({
  nombre: z.string().min(1, "Requerido"),
  apellido: z.string().min(1, "Requerido"),
  dni: z.string().min(7, "DNI inválido"),
  mail: z.string().email("Email inválido"),
  telefono: z.string().min(6, "Teléfono inválido"),
  direccion: z.string().min(5, "Dirección requerida"),
})

type FormValues = z.infer<typeof formSchema>

const ARCHIVO_LABELS: Record<TipoTramite, [string, string]> = {
  ALTA: ["Copia del DNI", "Comprobante de domicilio (impuesto)"],
  BAJA: ["Copia del DNI del titular", "Copia de la última factura"],
}

export function FormularioPage() {
  const [paso, setPaso] = useState(1)
  const [tipo, setTipo] = useState<TipoTramite>("ALTA")
  const [archivo1, setArchivo1] = useState<ArchivoResponse | null>(null)
  const [archivo2, setArchivo2] = useState<ArchivoResponse | null>(null)
  const [subiendo, setSubiendo] = useState<number | null>(null)
  const [enviando, setEnviando] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [resultado, setResultado] = useState<TramiteCreadoResponse | null>(null)

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      nombre: "",
      apellido: "",
      dni: "",
      mail: "",
      telefono: "",
      direccion: "",
    },
  })

  async function handleSubirArchivo(
    file: File | undefined,
    slot: 1 | 2
  ) {
    if (!file) return
    setError(null)
    setSubiendo(slot)
    try {
      const res = await subirArchivo(file)
      if (slot === 1) setArchivo1(res)
      else setArchivo2(res)
    } catch (e) {
      setError(getErrorMessage(e))
    } finally {
      setSubiendo(null)
    }
  }

  async function onSubmit(values: FormValues) {
    if (!archivo1 || !archivo2) {
      setError("Debés subir ambos archivos antes de enviar.")
      return
    }
    setEnviando(true)
    setError(null)
    try {
      const res = await crearTramite({
        tipo,
        ...values,
        archivo_id_1: archivo1.id,
        archivo_id_2: archivo2.id,
      })
      setResultado(res)
    } catch (e) {
      setError(getErrorMessage(e))
    } finally {
      setEnviando(false)
    }
  }

  if (resultado) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Trámite registrado</CardTitle>
          <CardDescription>
            {resultado.mensaje ??
              "Su trámite fue registrado. Recibirá un mail con su ID de seguimiento."}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Alert>
            <AlertTitle>ID de seguimiento</AlertTitle>
            <AlertDescription className="font-mono text-lg">
              {resultado.id}
            </AlertDescription>
          </Alert>
          <p className="text-sm text-muted-foreground">
            Guardá este código para consultar el estado en la sección
            &quot;Consultar estado&quot;.
          </p>
          <Button
            onClick={() => {
              setResultado(null)
              setPaso(1)
              setArchivo1(null)
              setArchivo2(null)
              form.reset()
            }}
          >
            Iniciar otro trámite
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Solicitud de trámite</CardTitle>
        <CardDescription>
          Completá los pasos para iniciar un trámite de alta o baja de servicio.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {error && (
          <Alert variant="destructive">
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {paso === 1 && (
          <div className="space-y-4">
            <Label>Tipo de trámite</Label>
            <div className="flex gap-3">
              {(["ALTA", "BAJA"] as TipoTramite[]).map((t) => (
                <Button
                  key={t}
                  type="button"
                  variant={tipo === t ? "default" : "outline"}
                  onClick={() => {
                    setTipo(t)
                    setArchivo1(null)
                    setArchivo2(null)
                  }}
                >
                  {t}
                </Button>
              ))}
            </div>
            <p className="text-sm text-muted-foreground">
              {tipo === "ALTA"
                ? "Alta de servicio: requiere DNI y comprobante de domicilio."
                : "Baja de servicio: requiere DNI del titular y última factura."}
            </p>
            <Button onClick={() => setPaso(2)}>Continuar</Button>
          </div>
        )}

        {paso === 2 && (
          <div className="space-y-4">
            <h3 className="font-medium">Documentación adjunta</h3>
            {[1, 2].map((slot) => {
              const archivo = slot === 1 ? archivo1 : archivo2
              const label = ARCHIVO_LABELS[tipo][slot - 1]
              return (
                <div key={slot} className="space-y-2 rounded-lg border p-4">
                  <Label>{label}</Label>
                  <Input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    disabled={subiendo !== null}
                    onChange={(e) =>
                      handleSubirArchivo(e.target.files?.[0], slot as 1 | 2)
                    }
                  />
                  {subiendo === slot && (
                    <p className="text-sm text-muted-foreground">Subiendo...</p>
                  )}
                  {archivo && (
                    <p className="text-sm text-green-700">
                      ✓ {archivo["nombre-archivo"]} ({archivo.id})
                    </p>
                  )}
                </div>
              )
            })}
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setPaso(1)}>
                Atrás
              </Button>
              <Button
                disabled={!archivo1 || !archivo2}
                onClick={() => setPaso(3)}
              >
                Continuar
              </Button>
            </div>
          </div>
        )}

        {paso === 3 && (
          <div className="space-y-4">
            <h3 className="font-medium">Datos personales</h3>
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-4"
              >
                <div className="grid gap-4 sm:grid-cols-2">
                  <FormField
                    control={form.control}
                    name="nombre"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Nombre</FormLabel>
                        <FormControl>
                          <Input {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="apellido"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Apellido</FormLabel>
                        <FormControl>
                          <Input {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <FormField
                  control={form.control}
                  name="dni"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>DNI</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="mail"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input type="email" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="telefono"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Teléfono</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="direccion"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Dirección</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <Separator />
                <div className="flex gap-2">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setPaso(2)}
                  >
                    Atrás
                  </Button>
                  <Button type="submit" disabled={enviando}>
                    {enviando ? "Enviando..." : "Enviar trámite"}
                  </Button>
                </div>
              </form>
            </Form>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
