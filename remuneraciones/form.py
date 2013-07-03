#encoding:utf-8
from django.forms import ModelForm


from remuneraciones.models import Pagos, Descuento

class PagosForm(ModelForm):
    class Meta:
        model = Pagos
        exclude = ['empleado']


class DescuentoForm(ModelForm):
    class Meta:
        model = Descuento
        exclude = ['empleado']