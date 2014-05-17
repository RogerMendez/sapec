from django.db import models

# Create your models here.
class Slide(models.Model):
    imagen = models.ImageField(upload_to="Slide", verbose_name="Seleccione Imagen")