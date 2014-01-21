from django.db import models
from django.contrib.auth.models import User
from personal.models import Persona
from organizacion.models import Cargo

class contratacion(models.Model):
    fecha_entrada = models.DateField(verbose_name="Fecha de inicio del Contrato", help_text="DIA/MES/AÑO")
    fecha_salida = models.DateField(verbose_name="Fecha Final del Contrato", help_text="DIA/MES/AÑO")
    sueldo = models.FloatField(verbose_name="Sueldo Del Empleado", help_text="hola como estas")
    descuento = models.FloatField(verbose_name="Descuento Por Falta", help_text="10 Retrasos equivalentes a una falta")
    estado = models.BooleanField(default=True)
    select = (
        (True,'SI'),
        (False, 'NO'),
    )
    permanente = models.BooleanField(default=False, choices=select)
    persona = models.ForeignKey(Persona)
    cargo = models.ForeignKey(Cargo)
    usuario = models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.empleado.nombre
    class Meta:
        verbose_name_plural = "Contrataciones"
        ordering = ['fecha_entrada']

