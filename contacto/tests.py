"""Pruebas de contacto: el formulario guarda el mensaje y valida los datos."""
from django.test import TestCase
from django.urls import reverse

from .models import Contacto


class PruebasContacto(TestCase):
    datos_validos = {
        "nombre": "Ana",
        "apellidos": "García",
        "email": "ana@ejemplo.com",
        "asunto": "Presupuesto",
        "mensaje": "Quisiera información.",
    }

    def test_mensaje_valido_se_guarda_y_redirige_a_gracias(self):
        respuesta = self.client.post(reverse("contacto:contacto"), self.datos_validos)

        self.assertRedirects(respuesta, reverse("contacto:gracias"))
        self.assertEqual(Contacto.objects.get().asunto, "Presupuesto")

    def test_campos_obligatorios_y_email_valido(self):
        datos = {**self.datos_validos, "nombre": "", "email": "no-es-un-email"}

        respuesta = self.client.post(reverse("contacto:contacto"), datos)

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Contacto.objects.exists())

    def test_pagina_de_gracias_se_muestra(self):
        self.assertContains(self.client.get(reverse("contacto:gracias")), "Gracias")
