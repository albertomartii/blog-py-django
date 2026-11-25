"""Piezas comunes para los formularios de todas las apps."""
from django import forms


class EstiloBootstrapMixin:
    """Añade la clase form-control de Bootstrap 3 a los campos que la necesitan."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if not isinstance(campo.widget, (forms.CheckboxInput, forms.FileInput)):
                campo.widget.attrs["class"] = "form-control"
