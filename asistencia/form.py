#encoding:utf-8

from models import Asistencia, Permiso
from django.forms import ModelForm
from django import forms

class AsistenciaForm(forms.Form):
    ci = forms.IntegerField(label="Cedula de Identidad")

class FechasForm(forms.Form):
    fecha_ini = forms.DateField(label="Fecha Inicio", help_text="Dia/Mes/Año")
    fecha_fin = forms.DateField(label="Fecha Finalización", help_text="Dia/Mes/Año")


class PermisoForm(ModelForm):
    class Meta:
        model = Permiso
        exclude = ['usuario', 'persona']