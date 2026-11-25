"""Pruebas de usuarios: registro, login por email y logout."""
from django.test import TestCase
from django.urls import reverse

from .models import Usuario


class PruebasRegistro(TestCase):
    datos_validos = {
        "email": "Ana@Ejemplo.com",
        "nombre": "Ana",
        "password1": "clave-segura-123",
        "password2": "clave-segura-123",
        "acepto_terminos": "on",
    }

    def test_registro_crea_usuario_y_abre_sesion(self):
        respuesta = self.client.post(reverse("usuarios:registro"), self.datos_validos)

        self.assertRedirects(respuesta, reverse("galeria:inicio"))
        usuario = Usuario.objects.get()
        self.assertEqual(usuario.email, "ana@ejemplo.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), usuario.pk)

    def test_registro_exige_aceptar_terminos(self):
        datos = {**self.datos_validos}
        del datos["acepto_terminos"]

        respuesta = self.client.post(reverse("usuarios:registro"), datos)

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Usuario.objects.exists())

    def test_registro_rechaza_email_repetido_aunque_cambien_las_mayusculas(self):
        Usuario.objects.create_user("ana@ejemplo.com", "clave-segura-123", nombre="Ana")

        respuesta = self.client.post(reverse("usuarios:registro"), self.datos_validos)

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Usuario.objects.count(), 1)


class PruebasAcceso(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user("ana@ejemplo.com", "clave-segura-123", nombre="Ana")

    def test_login_con_email_sin_distinguir_mayusculas(self):
        respuesta = self.client.post(
            reverse("usuarios:login"),
            {"username": "ANA@ejemplo.com", "password": "clave-segura-123"},
        )

        self.assertRedirects(respuesta, reverse("galeria:inicio"))

    def test_login_con_clave_incorrecta_muestra_error(self):
        respuesta = self.client.post(
            reverse("usuarios:login"),
            {"username": "ana@ejemplo.com", "password": "otra"},
        )

        self.assertContains(respuesta, "no son correctos")

    def test_logout_solo_funciona_por_post(self):
        self.client.force_login(self.usuario)

        self.assertEqual(self.client.get(reverse("usuarios:logout")).status_code, 405)
        self.client.post(reverse("usuarios:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)
