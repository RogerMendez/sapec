__author__ = 'Roger'

#encoding:utf-8
from django.forms import ModelForm
from django import forms
from models import Pagos, Descuentos

class PagosForm(ModelForm):
    class Meta:
        model = Pagos
        exclude = ['usuario', 'contrato']


class DescuentosForm(ModelForm):
    class Meta:
        model = Descuentos
        exclude = ['usuario', 'contrato']