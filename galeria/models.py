"""Modelos de la galería: categorías e imágenes."""
from django.core.validators import FileExtensionValidator
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField("nombre", max_length=255)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Imagen(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        verbose_name="categoría",
        on_delete=models.CASCADE,
        related_name="imagenes",
    )
    archivo = models.ImageField(
        "archivo",
        upload_to="galeria/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    numero_likes = models.PositiveIntegerField("likes", default=0)
    numero_visitas = models.PositiveIntegerField("visitas", default=0)
    numero_descargas = models.PositiveIntegerField("descargas", default=0)

    class Meta:
        verbose_name = "imagen"
        verbose_name_plural = "imágenes"
        ordering = ["id"]

    def __str__(self):
        return self.archivo.name
