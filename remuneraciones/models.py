#encoding=utf-8

from django.db import models

from personal.models import Empleados

class Pagos(models.Model):
    razon = models.CharField(max_length='50', verbose_name='Razon Del Pago')
    pago = models.FloatField(verbose_name='Monto A Pagar', help_text='En Bolivianos')
    descripcion = models.TextField(verbose_name='Descripción Del Pago')
    fecha = models.DateField(auto_now_add=True)
    empleado = models.ForeignKey(Empleados)
    def __unicode__(self):
        return self.razon
    class Meta:
        ordering=['razon']
        verbose_name_plural = "Pagos"

class Descuento(models.Model):
    razon = models.CharField(max_length='50', verbose_name='Razon del Descuento')
    pago = models.FloatField(verbose_name='Monto A Descontar', help_text='En Bolivianos')
    descripcion = models.TextField(verbose_name='Descripción Del Descuento')
    fecha = models.DateField(auto_now_add=True)
    empleado = models.ForeignKey(Empleados)
    def __unicode__(self):
        return self.razon
    class Meta:
        ordering=['razon']
        verbose_name_plural = "Descuentos"