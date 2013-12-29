from organizacion.models import Unidad, Cargo
from django.contrib.auth.models import Permission
from django.contrib import admin

admin.site.register(Unidad)
admin.site.register(Cargo)
admin.site.register(Permission)