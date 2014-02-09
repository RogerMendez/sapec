# -*- coding: utf-8 -*-
from django.db import models
from personal.models import Persona
from django.contrib.auth.models import User

class Asistencia(models.Model):
    fecha = models.DateField(auto_now_add=True)
    entrada_m = models.TimeField(blank=True, null=True, verbose_name="Hora Entrada Mañana")
    salida_m = models.TimeField(blank=True, null=True, verbose_name="Hora Salida Mañana")
    entrada_t = models.TimeField(blank=True, null=True, verbose_name="Hora Entrada Tarde")
    salida_t = models.TimeField(blank=True, null=True, verbose_name="Hora Salida Tarde")
    horas_realizadas = models.TimeField(blank=True, null=True, default="00:00")
    atraso = models.TimeField(blank=True, null=True)
    persona = models.ForeignKey(Persona)
    def __unicode__(self):
        return self.persona.nombre
    class Meta:
        verbose_name_plural = "Asistencia"
        ordering = ['fecha']
        permissions=(
            ("detail_asistencia", "Detalle Asistencia"),
        )


class Permiso(models.Model):
    descripcion = models.TextField(verbose_name="Razón del Permiso")
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_permiso = models.DateField(verbose_name="Fecha del Permiso", help_text="Dia/Mes/Año")
    inicio = models.TimeField(verbose_name="Hora de Inicio del Permiso")
    finalizacion = models.TimeField(verbose_name="Hora de Finzalización del Permiso")
    persona = models.ForeignKey(Persona, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.persona.nombre
    class Meta:
        ordering=['persona']
        verbose_name_plural = "Permisos"


