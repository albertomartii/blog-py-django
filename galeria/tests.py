"""Pruebas de la galería: portada pública y permisos de la zona de administración."""
import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image as ImagenPillow

from usuarios.models import Usuario

from .models import Categoria, Imagen

DIRECTORIO_MEDIA_TEMPORAL = tempfile.mkdtemp()


def crear_archivo_de_imagen(nombre="foto.png", formato="PNG"):
    contenido = BytesIO()
    ImagenPillow.new("RGB", (4, 4), "red").save(contenido, formato)
    return SimpleUploadedFile(nombre, contenido.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=DIRECTORIO_MEDIA_TEMPORAL)
class PruebasGaleria(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(DIRECTORIO_MEDIA_TEMPORAL, ignore_errors=True)

    def setUp(self):
        self.administrador = Usuario.objects.create_user("admin@ejemplo.com", "clave-segura-123", nombre="Admin", is_staff=True)
        self.usuario_normal = Usuario.objects.create_user("ana@ejemplo.com", "clave-segura-123", nombre="Ana")

    def test_portada_sin_categorias_no_falla(self):
        respuesta = self.client.get(reverse("galeria:inicio"))

        self.assertContains(respuesta, "Todavía no hay categorías")

    def test_portada_muestra_categorias_e_imagenes(self):
        categoria = Categoria.objects.create(nombre="Bodas")
        Imagen.objects.create(categoria=categoria, archivo=crear_archivo_de_imagen())

        respuesta = self.client.get(reverse("galeria:inicio"))

        self.assertContains(respuesta, "Bodas")
        self.assertContains(respuesta, "/media/galeria/foto")

    def test_zona_admin_redirige_al_login_si_no_hay_sesion(self):
        for nombre_ruta in ("galeria:categorias", "galeria:imagenes"):
            url = reverse(nombre_ruta)
            self.assertRedirects(self.client.get(url), f"{reverse('usuarios:login')}?next={url}")

    def test_zona_admin_prohibida_para_usuarios_sin_permisos(self):
        self.client.force_login(self.usuario_normal)

        for nombre_ruta in ("galeria:categorias", "galeria:imagenes"):
            self.assertEqual(self.client.get(reverse(nombre_ruta)).status_code, 403)

    def test_administrador_crea_categoria(self):
        self.client.force_login(self.administrador)

        respuesta = self.client.post(reverse("galeria:categorias"), {"nombre": "Paisajes"})

        self.assertRedirects(respuesta, reverse("galeria:categorias"))
        self.assertTrue(Categoria.objects.filter(nombre="Paisajes").exists())

    def test_administrador_sube_imagen(self):
        self.client.force_login(self.administrador)
        categoria = Categoria.objects.create(nombre="Retratos")

        respuesta = self.client.post(reverse("galeria:imagenes"), {
            "archivo": crear_archivo_de_imagen(),
            "categoria": categoria.pk,
            "numero_likes": 0,
            "numero_visitas": 0,
            "numero_descargas": 0,
        })

        self.assertRedirects(respuesta, reverse("galeria:imagenes"))
        self.assertEqual(Imagen.objects.get().categoria, categoria)

    def test_rechaza_archivos_que_no_son_jpg_o_png(self):
        self.client.force_login(self.administrador)
        categoria = Categoria.objects.create(nombre="Retratos")
        falso = SimpleUploadedFile("documento.pdf", b"%PDF-1.4", content_type="application/pdf")

        respuesta = self.client.post(reverse("galeria:imagenes"), {
            "archivo": falso,
            "categoria": categoria.pk,
            "numero_likes": 0,
            "numero_visitas": 0,
            "numero_descargas": 0,
        })

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Imagen.objects.exists())
