"""Carga las publicaciones de ejemplo en el blog. Se puede repetir sin crear duplicados."""
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from blog.datos_iniciales import PUBLICACIONES_INICIALES
from blog.models import Publicacion
from usuarios.models import Usuario

DIAS_ENTRE_PUBLICACIONES = 3


class Command(BaseCommand):
    help = "Carga las publicaciones de ejemplo definidas en blog/datos_iniciales.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--autor",
            help="Email del usuario que figurará como autor (por defecto, el primer superusuario)",
        )

    def handle(self, *args, **opciones):
        autor = self._buscar_autor(opciones["autor"])
        ahora = timezone.now()
        creadas = 0

        for posicion, datos in enumerate(PUBLICACIONES_INICIALES):
            # La primera de la lista es la más reciente; el resto se escalonan hacia atrás
            fecha = ahora - timedelta(days=posicion * DIAS_ENTRE_PUBLICACIONES)
            _, fue_creada = Publicacion.objects.get_or_create(
                titulo=datos["titulo"],
                defaults={
                    "contenido": datos["contenido"],
                    "imagen": datos["imagen"],
                    "autor": autor,
                    "fecha_publicacion": fecha,
                },
            )
            creadas += fue_creada

        omitidas = len(PUBLICACIONES_INICIALES) - creadas
        self.stdout.write(self.style.SUCCESS(f"Publicaciones creadas: {creadas}. Ya existían: {omitidas}."))

    def _buscar_autor(self, email):
        if email:
            try:
                return Usuario.objects.get(email__iexact=email)
            except Usuario.DoesNotExist:
                raise CommandError(f"No existe ningún usuario con el email {email}")
        return Usuario.objects.filter(is_superuser=True).order_by("id").first()
