# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from personal.models import Persona
from organizacion.models import Cargo

from django.db.models import Sum

class Contratacion(models.Model):
    fecha_entrada = models.DateField(verbose_name="Fecha de inicio del Contrato", help_text=u"DIA/MES/AÑO")
    fecha_salida = models.DateField(verbose_name="Fecha Final del Contrato", help_text=u"DIA/MES/AÑO")
    sueldo = models.FloatField(verbose_name="Sueldo Del Empleado", help_text="En Bolivianos")
    descuento = models.FloatField(verbose_name="Descuento Por Falta", help_text="10 Retrasos equivalentes a una falta")
    estado = models.BooleanField(default=True)
    select = (
        (True,'SI'),
        (False, 'NO'),
    )
    permanente = models.BooleanField(default=False, choices=select)
    persona = models.ForeignKey(Persona, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.persona.nombre
    class Meta:
        verbose_name_plural = "Contrataciones"
        ordering = ['fecha_entrada']
        permissions=(
            ("view_contrato", "Mostrar Contrato Persona"),
            ("show_contrato", "Mostrar Contratos Vigentes"),
        )
    def calcular_pago(self):
        from remuneraciones.models import Pagos
        #pagos = Pagos.objects.filter(contrato_id = self.id).aggregate(Sum('pago'))
        pagos = Pagos.objects.filter(contrato_id = self.id).aggregate(Sum('pago'))
        return pagos

class Movilidad(models.Model):
    contrato = models.ForeignKey(Contratacion,null=True, blank=True)
    cargo = models.ForeignKey(Cargo, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField(verbose_name=u'Razòn del Cambio', null=True)
    def __unicode__(self):
        return self.contrato.persona.nombre
    class Meta:
        verbose_name_plural = "Movilidad de Empleados"


class Terminar(models.Model):
    contrato = models.ForeignKey(Contratacion, null=True, blank=True)
    descripcion = models.TextField(verbose_name=u'Razon de Finalizaciòn Contrato', null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.contrato.persona.nombre
    class Meta:
        verbose_name_plural = "Contratos Terminados"

