# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from contratacion.models import Contratacion

class Pagos(models.Model):
    razon = models.CharField(max_length='50', verbose_name='Razon Del Pago')
    pago = models.FloatField(verbose_name='Monto A Pagar', help_text='En Bolivianos')
    descripcion = models.TextField(verbose_name='Descripción Del Pago')
    fecha = models.DateField(auto_now_add=True)
    contrato = models.ForeignKey(Contratacion, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __str__(self):
        return self.contrato.persona.nombre
    def __unicode__(self):
        return self.contrato.persona.nombre
    class Meta:
        ordering=['fecha']
        verbose_name_plural = "Pagos"


class Descuentos(models.Model):
    razon = models.CharField(max_length='50', verbose_name='Razon del Descuento')
    monto = models.FloatField(verbose_name='Monto A Descontar', help_text='En Bolivianos')
    descripcion = models.TextField(verbose_name='Descripción Del Descuento')
    fecha = models.DateField(auto_now_add=True)
    contrato = models.ForeignKey(Contratacion, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __str__(self):
        return self.razon
    def __unicode__(self):
        return self.razon
    class Meta:
        ordering=['fecha']
        verbose_name_plural = "Descuentos"