"""
Ajustes globales del proyecto.

Los valores sensibles o que cambian entre máquinas (clave secreta, modo
depuración, hosts permitidos) se leen de variables de entorno. Si no existen,
se usan valores seguros para desarrollo local.
"""
import os
from pathlib import Path

from django.contrib.messages import constants as niveles_mensaje

# Carpeta raíz del proyecto (la que contiene manage.py)
DIRECTORIO_BASE = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Seguridad
# ---------------------------------------------------------------------------

# En producción hay que definir DJANGO_SECRET_KEY; esta clave es solo para desarrollo
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "clave-solo-para-desarrollo-cambiar-en-produccion")

# DEBUG activo por defecto; en producción: DJANGO_DEBUG=0
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

# Lista separada por comas, p. ej. DJANGO_ALLOWED_HOSTS="midominio.com,127.0.0.1"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]


# ---------------------------------------------------------------------------
# Aplicaciones
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    # Aplicaciones propias
    "usuarios",
    "blog",
    "galeria",
    "contacto",
    # Aplicaciones incluidas en Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# ---------------------------------------------------------------------------
# Plantillas
# ---------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Plantillas globales (base.html y parciales comunes); las de cada app
        # se buscan en <app>/templates/<app>/ gracias a APP_DIRS
        "DIRS": [DIRECTORIO_BASE / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Bootstrap 3 llama "danger" a las alertas de error
MESSAGE_TAGS = {niveles_mensaje.ERROR: "danger"}


# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DIRECTORIO_BASE / "db.sqlite3",
    }
}


# ---------------------------------------------------------------------------
# Autenticación
# ---------------------------------------------------------------------------

# Usuario propio que se identifica por email (ver usuarios/models.py).
# Debe definirse antes de la primera migración.
AUTH_USER_MODEL = "usuarios.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 6},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Rutas a las que redirigen @login_required y las vistas de login/logout.
# Los nombres tienen formato "<namespace>:<nombre>" y se definen en cada urls.py
LOGIN_URL = "usuarios:login"
LOGIN_REDIRECT_URL = "galeria:inicio"
LOGOUT_REDIRECT_URL = "galeria:inicio"


# ---------------------------------------------------------------------------
# Internacionalización
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Archivos estáticos y subidos por los usuarios
# ---------------------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [DIRECTORIO_BASE / "static"]

# Imágenes de la galería subidas desde la zona de administración
MEDIA_URL = "media/"
MEDIA_ROOT = DIRECTORIO_BASE / "media"


# ---------------------------------------------------------------------------
# Ajustes propios del blog
# ---------------------------------------------------------------------------

PUBLICACIONES_POR_PAGINA = 5

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
