#encoding:utf-8
from django.forms import ModelForm
from django import forms
from organizacion.models import Unidades, Planificacion, Cargos, Funciones, Conocimiento

class UnidadForm(ModelForm):
    class Meta:
        model = Unidades

class PlanificacionForm(ModelForm):
    class Meta:
        model = Planificacion

class CargoForm(ModelForm):
    class Meta:
        model = Cargos

class FuncionForm(ModelForm):
    class Meta:
        model = Funciones

class ConocimientoForm(ModelForm):
    class Meta:
        model = Conocimiento
