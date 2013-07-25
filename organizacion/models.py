#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Unidades(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=False, blank=False)
    documento=models.FileField(upload_to='doc', verbose_name="Seleccionar Documento")
    def __unicode__(self):
        return self.nombre
    def __str__(self):
        return self.nombre
    class Meta:
        ordering=["nombre"]
        verbose_name_plural = "Unidades"

class Cargos(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=False)
    unidad = models.ForeignKey(Unidades, verbose_name="Unidad A La Que Pertenece")
    def __unicode__(self):
        return self.unidad.nombre + " - " + self.nombre
    def __str__(self):
        return self.unidad.nombre + " - " + self.nombre
    class Meta:
        ordering=["nombre"]
        verbose_name_plural = "Cargos"

class Planificacion(models.Model):
    descripcion = models.TextField()
    cantidad = models.IntegerField(default='1')
    fecha_plani = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True, verbose_name='Estado de la planificación', help_text='Activo / Inactivo')
    cargo = models.ForeignKey(Cargos, verbose_name='Unidad - Cargo')
    def __unicode__(self):
        return self.descripcion
    def __str__(self):
        return self.descripcion
    class Meta:
        ordering=['fecha_plani']
        verbose_name_plural = "Planificación"

class Funciones(models.Model):
    descripcion = models.TextField(null=False, blank=False, verbose_name='Descripción de la Función')
    estado = models.BooleanField(default=True,verbose_name="Estado De la Función", help_text="Activo / Inactivo"  )
    cargo = models.ForeignKey(Cargos, verbose_name='Unidad - Cargo Al que Pertenece')
    def __unicode__(self):
        return  self.descripcion
    def __str__(self):
        return  self.descripcion
    class Meta:
        verbose_name_plural = "Funciones"


class Conocimiento(models.Model):
    descripcion = models.TextField(null=False, blank=False, verbose_name='Descripción del Conocimiento')
    estado = models.BooleanField(default=True,verbose_name="Estado Del Conocimiento", help_text="Activo / Inactivo"  )
    cargo = models.ForeignKey(Cargos, verbose_name='Unidad - Cargo al que Pertenece')
    def __unicode__(self):
        return  self.descripcion
    def __str__(self):
        return  self.descripcion
    class Meta:
        verbose_name_plural = "Conocimiento"