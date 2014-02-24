#encoding:utf-8
from django.forms import ModelForm
from django import forms
from models import Contratacion, Movilidad, Terminar
from personal.models import Persona

class ContratacionEventualForm(ModelForm):
    class Meta:
        model = Contratacion
        exclude = ['usuario', 'persona', 'cargo', 'permanente', 'estado']

class PersonaSearchForm(forms.Form):
    texto = forms.CharField(label="Buscar Persona", help_text="Busqueda Por Cedula de Identidad", required=False)

class RazonCambioForm(ModelForm):
    class Meta:
        model = Movilidad
        exclude = ['contrato', 'cargo']

class TerminarContratoForm(ModelForm):
    class Meta:
        model = Terminar
        exclude = ['contrato', 'usuario']

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        exclude = ['completo', 'code_activation', 'usuario', 'foto']