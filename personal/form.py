#encoding:utf-8
from django.forms import ModelForm
from django import forms

from personal.models import Empleados, profesion, Observacion, Permiso
from organizacion.models import Cargos
from django.forms.extras.widgets import SelectDateWidget

class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleados
        exclude = ['usuario']

class ProfesionForm(ModelForm):
    class Meta:
        model=profesion


class Contrato(forms.Form):
    #widget = attr0
    fecha_fin = forms.DateField(label="Fin Del Contrato", help_text="Dia/Mes/Año")
    sueldo = forms.FloatField(label="Sueldo Empleado" ,help_text="En Bolivianos")
    descuento = forms.FloatField(label="Descuento Por Falta", help_text="Cada 10 Retrasos Una Falta")

    #cargo = Cargos.nombre


class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('pretty.css',)
        }
        js = ('animations.js', 'actions.js')


class AsistenciaForm(forms.Form):
    ci = forms.IntegerField(label="Cedula de Identidad");


class ObservacionForm(ModelForm):
    class Meta:
        model=Observacion
        exclude = ['empleado']

class PermisoForm(ModelForm):
    class Meta:
        model = Permiso
        exclude = ['empleado']