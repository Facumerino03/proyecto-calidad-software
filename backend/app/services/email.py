class EmailService:
    """Servicio de notificaciones por correo (stub para desarrollo)."""

    def enviar_id_seguimiento(self, mail: str, tracking_id: str) -> None:
        pass

    def enviar_cambio_estado(
        self,
        mail: str,
        tracking_id: str,
        estado: str,
        motivo: str | None = None,
    ) -> None:
        pass
