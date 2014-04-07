#encoding:utf-8

from models import Asistencia, Permiso
from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from datetime import datetime

class AsistenciaForm(forms.Form):
    ci = forms.IntegerField(label="Cedula de Identidad")

class FechasForm(forms.Form):
    fecha_ini = forms.DateField(label="Fecha Inicio", help_text="Dia/Mes/Año")
    fecha_fin = forms.DateField(label="Fecha Finalización", help_text="Dia/Mes/Año")


class PermisoForm(ModelForm):
    class Meta:
        model = Permiso
        exclude = ['usuario', 'persona']

class FechaSearchForm(forms.Form):
    fecha = forms.DateField(label="Seleccione una Fecha", help_text="Dia/Mes/Año", required=False)


class MonthSelect(forms.Form):
    hoy = datetime.now()
    anho = hoy.strftime("%Y")
    a_ini = int(anho) - 10
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
    mes = forms.ChoiceField(choices=meses, widget=forms.RadioSelect, label="Seleccione un Mes")


class YearSelect(forms.Form):
    hoy = datetime.now()
    anho = hoy.strftime("%Y")
    a_ini = int(anho) - 10
    a_fin = int(anho) + 1
    anhos = ()
    for a in range(a_ini, a_fin):
        anhos += ((a, a),)
    anho = forms.ChoiceField(choices=anhos, label=u'Seleccione Año')


class AsistenciaFormEdid(ModelForm):
    class Meta:
        model=Asistencia
        exclude=['fecha', 'persona']