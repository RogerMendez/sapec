#encoding:utf-8
from django.forms import ModelForm

from organizacion.models import Unidad, Cargo, Planificacion

class UnidadForm(ModelForm):
    class Meta:
        model = Unidad
        fields = '__all__'

class CargoForm(ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'

class PlanificacionForm(ModelForm):
    class Meta:
        model = Planificacion
        fields = '__all__'
#        exclude = ['usuario', 'estado']