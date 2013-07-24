from django.shortcuts import render_to_response, get_object_or_404

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson

from personal.models import Empleados, contratacion

from datetime import datetime


@dajaxice_register
def employee(request, carnet):
    dajax = Dajax()
    hoy = datetime.today()
    empleado = Empleados.objects.get(ci=carnet)
    q1 = contratacion.objects.filter(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO')
    q2 = q1.filter(empleado_id = empleado.id)
    if q2.count() > 0 :
        dajax.remove_css_class('div #hola1', 'hola')
        dajax.add_css_class('.btn2', 'btn1')
        return dajax.json()
    else:
        dajax.add_css_class('div #hola1', 'hola')
        dajax.remove_css_class('.btn1', 'btn1')
        nombre = empleado.nombre
        paterno = empleado.paterno
        materno = empleado.materno
        direccion = empleado.direccion
        telefono = empleado.telefono
        email = empleado.email
        nac = empleado.fecha_nac
        civil = empleado.estado_civil
        sexo = empleado.sexo
        fecha_nac = nac.strftime("%d/%m/%Y")
        profe = empleado.profesion_id
        dajax.assign('#id_nombre','value',str(nombre))
        dajax.assign('#id_paterno','value',str(paterno))
        dajax.assign('#id_materno','value',str(materno))
        dajax.assign('#id_direccion','value',str(direccion))
        dajax.assign('#id_telefono','value',str(telefono))
        dajax.assign('#id_email','value',str(email))
        dajax.assign('#id_fecha_nac','value',str(fecha_nac))
        data = [
            {'civil':civil, 'sexo':sexo,'profesion':profe }]
        dajax.add_data(data,'seleccionar')
        #dajax.add_data(sexo,'sexo')
        #dajax.assign('#id_nombre','value',str(nombre))
        return dajax.json()

@dajaxice_register
def verificarfechainicio(request, fecha_ini):
    dajax = Dajax()
    dajax.remove_css_class('div#hola1', 'hola')
    return  dajax.json()


@dajaxice_register
def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()