# PhotographItem: blog y galería con Django

Recreación del proyecto Symfony `blog-albertomarti` con la misma arquitectura:
MVC con plantillas renderizadas en servidor.

## Puesta en marcha

Requiere Python 3.10 o superior.

```bash
git pull
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser    # pide email, nombre y contraseña
python manage.py runserver
```

Para cargar 10 publicaciones de ejemplo en el blog (se pueden editar después desde `/admin/`):

```bash
python manage.py cargar_publicaciones                  # autor: el primer superusuario
python manage.py cargar_publicaciones --autor ana@ejemplo.com
```

Es seguro repetirlo: no duplica las publicaciones que ya existen. Los textos están en
`blog/datos_iniciales.py`.

Para ejecutar las pruebas: `python manage.py test`

## Estructura

| Carpeta | Contenido |
|---|---|
| `config/` | Ajustes (`settings.py`), URLs raíz y utilidades compartidas (formularios y permisos) |
| `usuarios/` | Usuario propio con login por email, registro y logout |
| `blog/` | Publicaciones, comentarios, búsqueda, paginación y likes |
| `galeria/` | Categorías, imágenes y su zona de administración |
| `contacto/` | Formulario de contacto guardado en base de datos |
| `templates/` | Plantilla base y parciales comunes |
| `static/` | Tema original: Bootstrap 3, jQuery, Font Awesome, CSS y JS |

Cada app guarda sus plantillas en `<app>/templates/<app>/`.

## Rutas

| URL | Qué hace | Acceso |
|---|---|---|
| `/` | Galería con una pestaña por categoría | Público |
| `/blog/` | Listado paginado; `?busqueda=` filtra por contenido, `?pagina=` cambia de página | Público |
| `/publicacion/<slug>/` | Detalle y comentarios | Público |
| `/publicacion/<slug>/like/` | Suma un like (solo POST, responde JSON) | Público |
| `/blog/nueva/` | Crear publicación | Con sesión |
| `/gestion/categorias/`, `/gestion/imagenes/` | Alta de categorías y subida de imágenes | Administradores |
| `/usuarios/entrar/`, `/usuarios/registro/` | Login y registro | Público |
| `/contacto/` | Formulario de contacto | Público |
| `/admin/` | Panel de Django (usuarios, publicaciones, imágenes, mensajes) | Administradores |

Un administrador es un usuario con `is_staff` (el equivalente a `ROLE_ADMIN`).

## Fallos del proyecto Symfony corregidos

- `Comment` sin importar y `$post->like()` inexistente: reescritos y con pruebas.
- Dos controladores con la misma ruta `app_categories`: ahora hay una sola vista.
- Nombres de propiedad con mayúscula en los repositorios: ya no hay consultas por nombre de texto.
- `/blog/new` sin protección y con autor nulo: exige sesión y el autor siempre es el usuario.
- El formulario de comentarios pedía publicación y fecha: ahora solo nombre, email y texto.
- Like por GET: ahora es POST con protección CSRF.
- Plantilla de detalle a medio hacer y parcial mal nombrado: completos.
- Slugs repetidos con títulos iguales: se generan únicos (`-2`, `-3`...).
- Contador de comentarios guardado aparte (podía desincronizarse): se calcula al consultar.
- Redirección a `/thankyou.html` (archivo inexistente): redirige a la vista de agradecimiento.
- Enlaces del menú a páginas HTML estáticas que no existen: sustituidos por rutas reales.

## Variables de entorno (opcionales en desarrollo)

| Variable | Uso |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta (obligatoria en producción) |
| `DJANGO_DEBUG` | `1` activa el modo depuración (por defecto), `0` lo desactiva |
| `DJANGO_ALLOWED_HOSTS` | Dominios permitidos, separados por comas |
