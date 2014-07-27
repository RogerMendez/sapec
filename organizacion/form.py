#encoding:utf-8
from django.forms import ModelForm

from organizacion.models import Unidad, Cargo, Planificacion

class UnidadForm(ModelForm):
    class Meta:
        model = Unidad

class CargoForm(ModelForm):
    class Meta:
        model = Cargo

class PlanificacionForm(ModelForm):
    class Meta:
        model = Planificacion
#        exclude = ['usuario', 'estado']