"""Pruebas del blog: slugs, permisos, paginación, búsqueda, comentarios, likes y carga inicial."""
from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase
from django.urls import reverse

from usuarios.models import Usuario

from .datos_iniciales import PUBLICACIONES_INICIALES
from .models import Comentario, Publicacion


def crear_publicacion(titulo="Título", contenido="Contenido", **extra):
    return Publicacion.objects.create(titulo=titulo, contenido=contenido, imagen="landscape.jpg", **extra)


class PruebasSlug(TestCase):
    def test_titulos_repetidos_generan_slugs_distintos(self):
        primera = crear_publicacion("Mi viaje a Ítaca")
        segunda = crear_publicacion("Mi viaje a Ítaca")
        tercera = crear_publicacion("Mi viaje a Ítaca")

        self.assertEqual(primera.slug, "mi-viaje-a-itaca")
        self.assertEqual(segunda.slug, "mi-viaje-a-itaca-2")
        self.assertEqual(tercera.slug, "mi-viaje-a-itaca-3")

    def test_el_slug_no_cambia_al_editar_la_publicacion(self):
        publicacion = crear_publicacion("Original")
        publicacion.titulo = "Editado"
        publicacion.save()

        self.assertEqual(publicacion.slug, "original")


class PruebasNuevaPublicacion(TestCase):
    datos = {"titulo": "Hola", "contenido": "Texto", "imagen": "family.jpg"}

    def test_visitante_anonimo_es_enviado_al_login(self):
        respuesta = self.client.post(reverse("blog:nueva"), self.datos)

        self.assertRedirects(respuesta, f"{reverse('usuarios:login')}?next={reverse('blog:nueva')}")
        self.assertFalse(Publicacion.objects.exists())

    def test_usuario_autenticado_queda_como_autor(self):
        usuario = Usuario.objects.create_user("ana@ejemplo.com", "clave-segura-123", nombre="Ana")
        self.client.force_login(usuario)

        respuesta = self.client.post(reverse("blog:nueva"), self.datos)

        publicacion = Publicacion.objects.get()
        self.assertRedirects(respuesta, reverse("blog:detalle", args=[publicacion.slug]))
        self.assertEqual(publicacion.autor, usuario)
        self.assertEqual(publicacion.numero_likes, 0)


class PruebasListado(TestCase):
    def setUp(self):
        for numero in range(1, 8):
            crear_publicacion(f"Publicación {numero}", contenido=f"Texto número {numero}")

    def test_listado_ordenado_de_mas_reciente_a_mas_antigua(self):
        respuesta = self.client.get(reverse("blog:listado"))

        titulos = [publicacion.titulo for publicacion in respuesta.context["pagina_actual"]]
        self.assertEqual(titulos, [f"Publicación {numero}" for numero in range(7, 2, -1)])

    def test_recientes_son_las_cinco_ultimas(self):
        respuesta = self.client.get(reverse("blog:listado"))

        titulos = [publicacion.titulo for publicacion in respuesta.context["recientes"]]
        self.assertEqual(titulos, [f"Publicación {numero}" for numero in range(7, 2, -1)])

    def test_pagina_con_cinco_publicaciones(self):
        respuesta = self.client.get(reverse("blog:listado"))

        self.assertEqual(len(respuesta.context["pagina_actual"]), 5)
        self.assertEqual(respuesta.context["total"], 7)

    def test_segunda_pagina_tiene_el_resto(self):
        respuesta = self.client.get(reverse("blog:listado"), {"pagina": 2})

        self.assertEqual(len(respuesta.context["pagina_actual"]), 2)

    def test_pagina_fuera_de_rango_o_invalida_no_rompe(self):
        fuera_de_rango = self.client.get(reverse("blog:listado"), {"pagina": 99})
        invalida = self.client.get(reverse("blog:listado"), {"pagina": "abc"})

        self.assertEqual(fuera_de_rango.context["pagina_actual"].number, 2)
        self.assertEqual(invalida.context["pagina_actual"].number, 1)

    def test_busqueda_filtra_por_contenido(self):
        respuesta = self.client.get(reverse("blog:listado"), {"busqueda": "número 3"})

        self.assertEqual(respuesta.context["total"], 1)
        self.assertContains(respuesta, "Publicación 3")

    def test_busqueda_sin_resultados_muestra_aviso(self):
        respuesta = self.client.get(reverse("blog:listado"), {"busqueda": "inexistente"})

        self.assertContains(respuesta, "No se han encontrado publicaciones")

    def test_la_paginacion_conserva_la_busqueda(self):
        respuesta = self.client.get(reverse("blog:listado"), {"busqueda": "Texto"})

        self.assertContains(respuesta, "?pagina=2&busqueda=Texto")


class PruebasDetalleYComentarios(TestCase):
    def setUp(self):
        self.publicacion = crear_publicacion("Con comentarios")
        self.url = reverse("blog:detalle", args=[self.publicacion.slug])

    def test_slug_inexistente_devuelve_404(self):
        self.assertEqual(self.client.get(reverse("blog:detalle", args=["no-existe"])).status_code, 404)

    def test_comentario_se_guarda_y_se_cuenta(self):
        datos = {"nombre": "Luis", "email": "luis@ejemplo.com", "texto": "Muy bueno"}

        respuesta = self.client.post(self.url, datos)

        self.assertRedirects(respuesta, self.url)
        self.assertEqual(Comentario.objects.get().publicacion, self.publicacion)
        total = Publicacion.objects.con_total_comentarios().get(pk=self.publicacion.pk).total_comentarios
        self.assertEqual(total, 1)

    def test_el_visitante_no_puede_elegir_publicacion_ni_fecha(self):
        otra = crear_publicacion("Otra")
        datos = {"nombre": "Luis", "email": "luis@ejemplo.com", "texto": "Hola", "publicacion": otra.pk}

        self.client.post(self.url, datos)

        self.assertEqual(Comentario.objects.get().publicacion, self.publicacion)

    def test_borrar_un_comentario_actualiza_el_total(self):
        Comentario.objects.create(publicacion=self.publicacion, nombre="A", email="a@a.es", texto="x")
        Comentario.objects.create(publicacion=self.publicacion, nombre="B", email="b@b.es", texto="y")
        Comentario.objects.filter(nombre="A").delete()

        total = Publicacion.objects.con_total_comentarios().get(pk=self.publicacion.pk).total_comentarios
        self.assertEqual(total, 1)

    def test_comentario_invalido_no_se_guarda(self):
        respuesta = self.client.post(self.url, {"nombre": "", "email": "no-es-email", "texto": ""})

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Comentario.objects.exists())

    def test_publicacion_sin_autor_se_muestra(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)


class PruebasLikes(TestCase):
    def setUp(self):
        self.publicacion = crear_publicacion("Con likes")
        self.url = reverse("blog:like", args=[self.publicacion.slug])

    def test_get_no_modifica_datos(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

        self.publicacion.refresh_from_db()
        self.assertEqual(self.publicacion.numero_likes, 0)

    def test_post_suma_un_like_y_devuelve_json(self):
        self.client.post(self.url)
        respuesta = self.client.post(self.url)

        self.assertEqual(respuesta.json(), {"correcto": True, "likes": 2})

    def test_like_a_slug_inexistente_devuelve_404(self):
        self.assertEqual(self.client.post(reverse("blog:like", args=["no-existe"])).status_code, 404)


class PruebasCargaInicial(TestCase):
    def cargar(self, *argumentos):
        call_command("cargar_publicaciones", *argumentos, stdout=StringIO())

    def test_las_imagenes_de_los_datos_existen_en_static(self):
        from pathlib import Path

        from django.conf import settings

        for datos in PUBLICACIONES_INICIALES:
            archivo = Path(settings.DIRECTORIO_BASE) / "static" / "images" / "blog" / datos["imagen"]
            self.assertTrue(archivo.exists(), f"Falta la imagen {datos['imagen']}")

    def test_crea_diez_publicaciones_ordenadas_por_fecha(self):
        self.cargar()

        self.assertEqual(Publicacion.objects.count(), 10)
        primera = Publicacion.objects.first()
        self.assertEqual(primera.titulo, PUBLICACIONES_INICIALES[0]["titulo"])

    def test_se_puede_repetir_sin_duplicar(self):
        self.cargar()
        self.cargar()

        self.assertEqual(Publicacion.objects.count(), 10)

    def test_asigna_el_autor_indicado(self):
        usuario = Usuario.objects.create_user("ana@ejemplo.com", "clave-segura-123", nombre="Ana")

        self.cargar("--autor", "ANA@ejemplo.com")

        self.assertEqual(Publicacion.objects.filter(autor=usuario).count(), 10)

    def test_por_defecto_usa_el_primer_superusuario(self):
        admin = Usuario.objects.create_superuser("admin@ejemplo.com", "clave-segura-123", nombre="Admin")

        self.cargar()

        self.assertEqual(Publicacion.objects.filter(autor=admin).count(), 10)

    def test_autor_inexistente_da_error(self):
        with self.assertRaises(CommandError):
            self.cargar("--autor", "nadie@ejemplo.com")
