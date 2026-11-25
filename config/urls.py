"""
URLs raíz del proyecto.

Cada app define sus propias rutas en su urls.py y aquí solo se enlazan.
El namespace (app_name en cada urls.py) permite referenciar las rutas
como "blog:listado", "usuarios:login", etc.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("usuarios/", include("usuarios.urls")),
    path("contacto/", include("contacto.urls")),
    # Galería y blog cuelgan de la raíz; sus rutas no se solapan
    path("", include("galeria.urls")),
    path("", include("blog.urls")),
]

# En desarrollo, Django sirve las imágenes subidas; en producción lo hace el servidor web
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
