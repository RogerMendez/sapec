#encoding:utf-8
from django.forms import ModelForm

from personal.models import Persona, Estudios, OtrosEstudios, Experiencias

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        exclude = ['code_activation','usuario', 'completo']

class EstudiosForm(ModelForm):
    class Meta:
        model = Estudios
        exclude = ['persona']

class OtrosEstudiosForm(ModelForm):
    class Meta:
        model = OtrosEstudios
        exclude = {'persona'}

class ExperienciasForm(ModelForm):
    class Meta:
        model = Experiencias
        exclude = ['persona']