#encoding:utf-8

from django.forms import ModelForm
from django import forms
from models import Pagos, Descuentos
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
import datetime

class PagosForm(ModelForm):
    class Meta:
        model = Pagos
        exclude = ['usuario', 'contrato']


class DescuentosForm(ModelForm):
    class Meta:
        model = Descuentos
        exclude = ['usuario', 'contrato']

class FechasPlanillaForm(forms.Form):
    hoy = datetime.datetime.now()
    anho = hoy.strftime("%Y")
    a_ini = 2000
    a_fin = int(anho) + 1
    anhos = ()
    for a in range(a_ini, a_fin):
        anhos += ((a, a),)
    anho = forms.ChoiceField(choices=anhos, label=u'Seleccione Año')
    meses = (
        ('01','Enero'),
        ('02','Febrero'),
        ('03','Marzo'),
        ('04','Abril'),
        ('05','Mayo'),
        ('06','Junio'),
        ('07','Julio'),
        ('08','Agosto'),
        ('09','Septiembre'),
        ('10','Octubre'),
        ('11','Noviembre'),
        ('12','Diciembre'),
    )
    mes = forms.ChoiceField(choices=meses, label="Seleccione un Mes")