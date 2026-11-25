"""Modelos del blog: publicaciones y sus comentarios."""
from django.conf import settings
from django.db import models
from django.db.models import Count, F
from django.templatetags.static import static
from django.utils import timezone
from django.utils.text import slugify


class ConsultasPublicacion(models.QuerySet):
    """Consultas reutilizables sobre publicaciones."""

    def con_total_comentarios(self):
        # El total se calcula al consultar: así nunca se desincroniza
        # al crear o borrar comentarios desde cualquier sitio.
        # Con un annotate agregado Django ignora Meta.ordering, por eso se
        # ordena de forma explícita (el id desempata fechas iguales).
        return self.annotate(total_comentarios=Count("comentarios")).order_by("-fecha_publicacion", "-id")


class Publicacion(models.Model):
    titulo = models.CharField("título", max_length=255)
    contenido = models.TextField("contenido")
    fecha_publicacion = models.DateTimeField("fecha de publicación", default=timezone.now)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="autor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="publicaciones",
    )
    imagen = models.CharField(
        "imagen",
        max_length=255,
        help_text="Nombre del archivo dentro de static/images/blog/ (por ejemplo, landscape.jpg).",
    )
    slug = models.SlugField("slug", max_length=255, unique=True, blank=True, editable=False)
    numero_likes = models.PositiveIntegerField("likes", default=0)

    objects = ConsultasPublicacion.as_manager()

    class Meta:
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generar_slug_unico()
        super().save(*args, **kwargs)

    def _generar_slug_unico(self):
        """Deriva el slug del título y añade -2, -3... si ya existe otro igual."""
        base = slugify(self.titulo)[:240] or "publicacion"
        slug_candidato = base
        contador = 2
        while Publicacion.objects.filter(slug=slug_candidato).exists():
            slug_candidato = f"{base}-{contador}"
            contador += 1
        return slug_candidato

    @property
    def url_imagen(self):
        return static(f"images/blog/{self.imagen}")

    def registrar_like(self):
        """Suma un like con una única operación en base de datos (segura ante concurrencia)."""
        Publicacion.objects.filter(pk=self.pk).update(numero_likes=F("numero_likes") + 1)
        self.refresh_from_db(fields=["numero_likes"])


class Comentario(models.Model):
    publicacion = models.ForeignKey(
        Publicacion,
        verbose_name="publicación",
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    nombre = models.CharField("nombre", max_length=255)
    email = models.EmailField("correo electrónico", max_length=255)
    texto = models.TextField("comentario")
    fecha_publicacion = models.DateTimeField("fecha de publicación", auto_now_add=True)

    class Meta:
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"
        ordering = ["fecha_publicacion"]

    def __str__(self):
        return f"{self.nombre} en «{self.publicacion}»"
