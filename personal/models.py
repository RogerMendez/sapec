#encoding=utf-8
from django.db import models
from organizacion.models import Cargos
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

def validate_min(value):
    if len(str(value)) != 8 and len(str(value)) != 7:
        raise ValidationError(u'%s No es Una Cedula de Identidad Valida' % value)

class profesion(models.Model):
    descripcion=models.TextField()
    def __unicode__(self):
        return self.descripcion
    class Meta:
        verbose_name_plural = "Profesiones"

class Empleados(models.Model):
    ci=models.IntegerField(max_length='9',validators=[validate_min], verbose_name="Cedula de Identidad", unique=False)
    paterno=models.CharField(max_length='50', verbose_name="Apellido Paterno")
    materno=models.CharField(max_length='50', null=True, blank=True, verbose_name="Apellido Materno")
    nombre=models.CharField(max_length='100', verbose_name="Nombres")
    direccion=models.CharField(max_length='100', null=True, blank=True, verbose_name="Dirección de Empleado")
    telefono=models.IntegerField(max_length='10', verbose_name="Telefono/Celular", null=True, blank=True)
    estado_civ=(
        ('SO', 'Soltero(a)'),
        ('CA', 'Casado(a)'),
    )
    estado_civil=models.CharField(max_length='2',choices=estado_civ, null=True, blank=True, verbose_name="Estado Civil")
    GRUPO_CHOICES = (
        ('FE', 'Femenino'),
        ('MA', 'Masculino'),

    )
    sexo = models.CharField(max_length=2, choices=GRUPO_CHOICES, verbose_name="Sexo", null=True, blank=True)
    fecha_nac=models.DateField(verbose_name="Fecha de Nacimiento", help_text="DIA/MES/AÑO", null=True, blank=True)
    email = models.EmailField(verbose_name='Dirección de Correo Electronico')
    foto = models.ImageField(upload_to='personal', verbose_name="Seleccionar Imagen", blank=True, null=True)
    profesion=models.ForeignKey(profesion)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.nombre + " " + self.paterno + " " + self.materno
    class Meta:
        ordering = ["ci"]
        verbose_name_plural = "Empleados"

class contratacion(models.Model):
    fecha_entrada = models.DateField(verbose_name="Fecha de inicio del Contrato", help_text="DIA/MES/AÑO")
    fecha_salida = models.DateField(verbose_name="Fecha Final del Contrato", help_text="DIA/MES/AÑO")
    estado = models.CharField(max_length='10', default='INACTIVO')
    sueldo = models.FloatField(verbose_name="Sueldo Del Empleado")
    descuento = models.FloatField(verbose_name="Descuento Por Falta", help_text="10 Retrasos equivalentes a una falta")
    empleado = models.ForeignKey(Empleados)
    cargo = models.ForeignKey(Cargos)
    def __unicode__(self):
        return self.empleado.nombre
    class Meta:
        verbose_name_plural = "Contrataciones"

class Asistencia(models.Model):
    fecha = models.DateField()
    entrada_m = models.TimeField(blank=True, null=True)
    salida_m = models.TimeField(blank=True, null=True)
    obs_m = models.CharField(max_length='15', blank=True, null=True)
    entrada_t = models.TimeField(blank=True, null=True)
    salida_t = models.TimeField(blank=True, null=True)
    obs_t = models.CharField(max_length="15", blank=True, null=True)
    empleado = models.ForeignKey(Empleados)
    def __unicode__(self):
        return self.empleado.nombre
    class Meta:
        verbose_name_plural = "Asistencia"
        ordering = ['fecha']

class Entrada(models.Model):
    hora = models.TimeField()
    obs = models.CharField(max_length="15", blank=True, null=True)
    asistencia = models.ForeignKey(Asistencia)
    def __unicode__(self):
        return self.asistencia.empleado
    class Meta:
        verbose_name_plural = "Entradas"

class Salida(models.Model):
    hora = models.TimeField()
    obs = models.CharField(max_length="15", blank=True, null=True)
    asistencia = models.ForeignKey(Asistencia)
    def __unicode__(self):
        return self.asistencia.empleado
    class Meta:
        verbose_name_plural = "Salidas"

class Observacion(models.Model):
    tipo_obs=(
                ('LA', 'Llamada De Atención'),
                ('ME', 'Memorandum'),
            )
    tipo = models.CharField(max_length='5', choices=tipo_obs, verbose_name="Seleccione el tipo de Observacion")
    descripcion=models.TextField(verbose_name="Descripción De La Observación")
    fecha = models.DateField(auto_now_add=True)
    empleado = models.ForeignKey(Empleados)
    def __unicode__(self):
        return self.tipo
    class Meta:
        ordering=['tipo']
        verbose_name_plural = "Observaciones"

class Permiso(models.Model):
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    tiempo = models.CharField(max_length='10')
    empleado = models.ForeignKey(Empleados)
    def __unicode__(self):
        return self.empleado.nombre
    class Meta:
        ordering=['empleado']
        verbose_name_plural = "Permisos"

class moviidad(models.Model):
    contrato = models.ForeignKey(contratacion)
    cargo = models.ForeignKey(Cargos)
    fecha = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return str(self.fecha)
    class Meta:
        verbose_name_plural = "Movimientos"
