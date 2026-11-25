"""Modelo de contacto: los mensajes del formulario se guardan en base de datos."""
from django.db import models


class Contacto(models.Model):
    nombre = models.CharField("nombre", max_length=255)
    apellidos = models.CharField("apellidos", max_length=255)
    email = models.EmailField("correo electrónico", max_length=255)
    asunto = models.CharField("asunto", max_length=255)
    mensaje = models.TextField("mensaje")

    class Meta:
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.asunto} ({self.email})"
