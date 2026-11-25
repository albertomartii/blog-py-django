"""Modelo de usuario propio: se identifica por email y tiene un nombre visible."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class GestorUsuarios(BaseUserManager):
    """Crea usuarios y superusuarios usando el email como identificador."""

    def get_by_natural_key(self, email):
        # El login no distingue mayúsculas de minúsculas en el email
        return self.get(email__iexact=email)

    def _crear_usuario(self, email, password, **campos_extra):
        if not email:
            raise ValueError("El email es obligatorio")
        usuario = self.model(email=self.normalize_email(email).lower(), **campos_extra)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, email, password=None, **campos_extra):
        campos_extra.setdefault("is_staff", False)
        campos_extra.setdefault("is_superuser", False)
        return self._crear_usuario(email, password, **campos_extra)

    def create_superuser(self, email, password=None, **campos_extra):
        campos_extra["is_staff"] = True
        campos_extra["is_superuser"] = True
        return self._crear_usuario(email, password, **campos_extra)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Usuario del sitio.

    is_staff equivale al ROLE_ADMIN de Symfony: da acceso a la zona de
    administración de la galería y al panel /admin/.
    """

    email = models.EmailField("correo electrónico", max_length=180, unique=True)
    nombre = models.CharField("nombre", max_length=255)
    is_active = models.BooleanField("activo", default=True)
    is_staff = models.BooleanField(
        "administrador",
        default=False,
        help_text="Permite acceder a las zonas de administración.",
    )

    objects = GestorUsuarios()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.nombre

    def get_short_name(self):
        return self.nombre
