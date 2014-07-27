# -*- coding: utf-8 -*-
from django.db import models
from personal.models import Persona
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

def validate_date(value):
    hoy = date.today()
    if value < hoy:
        raise ValidationError(u'La Fecha del Permiso no Puede ser Menor A La Fecha Actual')

class Asistencia(models.Model):
    fecha = models.DateField(auto_now_add=True)
    entrada_m = models.TimeField(blank=True, null=True, verbose_name="Hora Entrada Mañana")
    salida_m = models.TimeField(blank=True, null=True, verbose_name="Hora Salida Mañana")
    entrada_t = models.TimeField(blank=True, null=True, verbose_name="Hora Entrada Tarde")
    salida_t = models.TimeField(blank=True, null=True, verbose_name="Hora Salida Tarde")
    horas_realizadas = models.TimeField(blank=True, null=True, default="00:00")
    atraso = models.TimeField(blank=True, null=True)
    persona = models.ForeignKey(Persona)
    def __str__(self):
        return self.persona.nombre
    def __unicode__(self):
        return self.persona.nombre
    class Meta:
        verbose_name_plural = "Asistencia"
        ordering = ['fecha']
        permissions=(
            ("detail_asistencia", "Detalle Asistencia"),
            ("detail_fecha_asistencia", "Asistencia Por Fecha"),
            ("historial_month_asistencia", "Historial Mensual"),
            ("historial_year_asistencia", "Historial Anual"),
        )


class Permiso(models.Model):
    descripcion = models.TextField(verbose_name="Razón del Permiso")
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_permiso = models.DateField(verbose_name="Fecha del Permiso", validators=[validate_date], help_text="Dia/Mes/Año")
    inicio = models.TimeField(verbose_name="Hora de Inicio del Permiso")
    finalizacion = models.TimeField(verbose_name="Hora de Finzalización del Permiso")
    persona = models.ForeignKey(Persona, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.persona.nombre
    def __str__(self):
        return self.persona.nombre
    class Meta:
        ordering=['persona']
        verbose_name_plural = "Permisos"


class Horario(models.Model):
    entrada_m = models.TimeField()
    salida_m = models.TimeField()
    entrada_t = models.TimeField()
    salida_t = models.TimeField()
