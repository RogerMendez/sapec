#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_min(value):
    if len(str(value)) != 8 and len(str(value)) != 7:
        raise ValidationError(u'%s No es Una Cedula de Identidad Valida' % value)

class Persona(models.Model):
    ci = models.IntegerField(max_length='9',validators=[validate_min], verbose_name="Cedula de Identidad", unique=True, null=True)
    paterno = models.CharField(max_length='50', verbose_name="Apellido Paterno")
    materno = models.CharField(max_length='50', null=True, blank=True, verbose_name="Apellido Materno")
    nombre = models.CharField(max_length='100', verbose_name="Nombres")
    fecha_nac = models.DateField(verbose_name="Fecha de Nacimiento", help_text="DIA/MES/AÑO", null=True, blank=True)
    direccion = models.CharField(max_length='100', null=True, blank=True, verbose_name="Dirección de Empleado")
    telefono = models.IntegerField(max_length='10', verbose_name="Telefono/Celular", null=True, blank=True)
    estado_civ = (
        ('SO', 'Soltero(a)'),
        ('CA', 'Casado(a)'),
    )
    estado_civil = models.CharField(max_length='2',choices=estado_civ, null=True, blank=True, verbose_name="Estado Civil")
    sex = (
        ('FE', 'Femenino'),
        ('MA', 'Masculino'),
    )
    sexo = models.CharField(max_length=2, choices=sex, verbose_name="Sexo", null=True, blank=True)
    foto = models.ImageField(upload_to='personal', verbose_name="Seleccionar Imagen", blank=True, null=True)
    completo = models.BooleanField(default=False)
    code_activation = models.CharField(max_length="100")
    usuario = models.ForeignKey(User, null=True, blank=True, unique=True)
    def __unicode__(self):
        return self.nombre + " " + self.paterno + " " + self.materno
    class Meta:
        ordering = ["ci"]
        verbose_name_plural = "Empleados"
        permissions=(
            ("show_datos_persona", "Mostrar Datos de Persona"),
        )


class Estudios(models.Model):
    institucion = models.CharField(max_length='200', verbose_name="Nombre de La Institución")
    fecha_inicio = models.DateField(verbose_name="Desde", help_text="Día/Mes/Año")
    fecha_fin = models.DateField(verbose_name="Hasta", help_text="Día/Mes/Año")
    titulo = models.CharField(max_length='100', verbose_name='Titulo Obtenido', help_text="Ejemplo: Lic. En Contabilidad")
    persona = models.ForeignKey(Persona, null=True)
    def __unicode__(self):
        return self.institucion
    class Meta:
        verbose_name_plural = "Estudios"
        permissions=(
            ("show_estudios_persona", "Mostrar Estudios de Persona"),
        )

class OtrosEstudios(models.Model):
    curso = models.CharField(max_length="200", verbose_name="Nombre del Curso/Congreso Realizado")
    horas = models.IntegerField(verbose_name="Cantidad de Horas", help_text="En Horas")
    fecha = models.DateField(verbose_name="Fecha de Realizacion del Curso", help_text="Día/Mes/Año")
    persona = models.ForeignKey(Persona, null=True, blank=True)
    def __unicode__(self):
        return self.curso
    class Meta:
        verbose_name_plural = "Cursos Realizados"
        permissions=(
            ("show_otrosestudios_persona", "Mostrar Otros Estudios Realizados"),
        )


class Experiencias(models.Model):
    institucion = models.CharField(max_length='200', verbose_name=u'Nombre de la Institución en la que Trabajo')
    cargo_ocupado = models.CharField(max_length='100', verbose_name="Cargo Ocupado")
    descripcion = models.TextField(verbose_name=u'Descripción Del Trabajo Realizado', help_text="Sea Breve")
    fecha_inicio = models.DateField(verbose_name='Desde', help_text="Día/Mes/Año")
    fecha_fin = models.DateField(verbose_name="Hasta", help_text="Día/Mes/Año")
    fono_referencia = models.IntegerField(blank=True, null=True, verbose_name="Telefono de Referencia")
    persona = models.ForeignKey(Persona, null=True, blank=True)
    def __unicode__(self):
        return self.institucion
    class Meta:
        verbose_name_plural = "Experiencias de Trabajo"
        permissions = (
            ("show_experienciatrabajo_persona", "Mostrar Experiencias de Trabajo"),
        )

class Idiomas(models.Model):
    idioma = models.CharField(max_length='50', verbose_name="Idioma")
    select = (
        (True, 'Si'),
        (False, 'No'),
    )
    nativo = models.BooleanField(choices=select)
    habla = models.BooleanField(choices=select)
    escribe = models.BooleanField(choices=select)
    persona = models.ForeignKey(Persona,null=True, blank=True)
    def __unicode__(self):
        return self.idioma
    class Meta:
        verbose_name_plural = "Idiomas"
        permissions = (
            ("show_idiomas_persona", "Mostrar Idiomas de Persona"),
        )

class Observacion(models.Model):
    tipo_obs=(
        ('LA', 'Llamada De Atención'),
        ('ME', 'Memorandum'),
    )
    tipo = models.CharField(max_length='5', choices=tipo_obs, verbose_name="Seleccione el tipo de Observacion")
    descripcion=models.TextField(verbose_name="Descripción De La Observación")
    fecha = models.DateField(auto_now_add=True)
    persona = models.ForeignKey(Persona, null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.persona.nombre
    class Meta:
        ordering=['persona']
        verbose_name_plural = "Observaciones"


