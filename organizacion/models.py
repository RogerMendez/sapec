#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

from organizacion.filefield import ContentTypeRestrictedFileField

class Unidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Unidad")
    descripcion = models.TextField(null=False, blank=False, verbose_name="Breve Descripción de la Unidad")
    documento=models.FileField(upload_to='unidad', verbose_name="Seleccionar Documento de Unidad", help_text="Archivo de PDF")
    #documento = models.FileField()
    def __unicode__(self):
        return self.nombre
    def __str__(self):
        return self.nombre
    class Meta:
        ordering=["nombre"]
        verbose_name_plural = "Unidades"
        permissions = (
            ("view_detail_unidad", "Ver Detalle Unidad"),
            ("list_unidad_pdf", "Listado Unidades PDF"),
            ("unidades_sin_cargo", "Listado Unidades Sin Cargo"),
        )


class Cargo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre de Cargo", unique=False)
    descripcion = models.TextField(verbose_name="Breve Descripción del Cargo")
    documento=models.FileField(upload_to='unidad', verbose_name="Seleccionar Documento de Cargo", help_text="Archivo de PDF")
    unidad = models.ForeignKey(Unidad, null=True, blank=True)
    def __unicode__(self):
        return self.unidad.nombre + " - " + self.nombre
    def __str__(self):
        return self.unidad.nombre + " - " + self.nombre
    class Meta:
        ordering=["unidad"]
        verbose_name_plural = "Cargos"
        permissions = (
            ("detail_cargo", "Ver Detalle Cargo"),
            ("list_cargos_pdf", "Listado Cargos PDF"),
        )

class Planificacion(models.Model):
    descripcion = models.TextField(verbose_name='Descripción de la Planificación')
    cantidad = models.IntegerField(default='1', verbose_name="Cantidad de Personal Requerido")
    fecha_plani = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True, verbose_name='Estado de la planificación', help_text='Activo / Inactivo')
    cargo = models.ForeignKey(Cargo, verbose_name='Unidad - Cargo')
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.descripcion
    def __str__(self):
        return self.descripcion
    class Meta:
        ordering=['fecha_plani']
        verbose_name_plural = "Planificación"
        permissions=(
            ("detail_planificacion", "Ver Detalle Planificación"),
            ("cancel_planificacion", "Cancelar Planificación"),
            ("plani_cargo", "Planificaciones Por Cargo"),
        )


