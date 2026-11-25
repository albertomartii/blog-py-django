"""Formularios de usuarios: registro público y formularios del panel /admin/."""
from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm

from config.formularios import EstiloBootstrapMixin

from .models import Usuario


class FormularioRegistro(EstiloBootstrapMixin, BaseUserCreationForm):
    """Alta de usuario con email, nombre, contraseña y aceptación de términos."""

    acepto_terminos = forms.BooleanField(
        label="Acepto los términos de uso",
        error_messages={"required": "Debes aceptar los términos para registrarte."},
    )

    class Meta:
        model = Usuario
        fields = ("email", "nombre")

    def clean_email(self):
        return self.cleaned_data["email"].lower()


class FormularioCreacionUsuarioAdmin(BaseUserCreationForm):
    """Alta de usuarios desde /admin/ (el predeterminado exige un campo username)."""

    class Meta:
        model = Usuario
        fields = ("email", "nombre")


class FormularioEdicionUsuarioAdmin(UserChangeForm):
    """Edición de usuarios desde /admin/ sobre el modelo propio."""

    class Meta:
        model = Usuario
        fields = "__all__"
