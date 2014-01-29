#encoding:utf-8
from django.forms import ModelForm
from django import forms

from personal.models import Persona, Estudios, OtrosEstudios, Experiencias, Idiomas

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

class IdiomasForm(forms.ModelForm):
    nativo = forms.ChoiceField(choices=Idiomas.select, widget=forms.RadioSelect)
    habla = forms.ChoiceField(choices=Idiomas.select, widget=forms.RadioSelect)
    escribe = forms.ChoiceField(choices=Idiomas.select, widget=forms.RadioSelect)
    class Meta:
        model = Idiomas
        #widgets = {'nativo': forms.RadioSelect}
        #nativo = forms.CheckboxSelectMultiple(choices=Idiomas.select,  widget=forms.CheckboxSelectMultiple())
        exclude = ['persona']