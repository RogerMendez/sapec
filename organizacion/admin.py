from organizacion.models import Unidades, Planificacion, Funciones, Cargos
from django.contrib.auth.models import Group, Permission
from django.contrib import admin



admin.site.register(Unidades)
admin.site.register(Planificacion)
admin.site.register(Funciones)
admin.site.register(Cargos)
admin.site.register(Permission)