"""Decoradores de acceso compartidos por las vistas de administración."""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def solo_administradores(vista):
    """
    Restringe una vista a usuarios con is_staff.

    Un visitante anónimo es enviado al login; un usuario autenticado sin
    permisos recibe un 403.
    """

    @wraps(vista)
    @login_required
    def vista_protegida(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return vista(request, *args, **kwargs)

    return vista_protegida
