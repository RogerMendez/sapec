#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from personal.models import Empleados, contratacion, Asistencia
from remuneraciones.models import Pagos, Descuento
from remuneraciones.form import PagosForm, DescuentoForm

from django.contrib.auth.decorators import login_required

from django.db.models import Count, Sum, Avg, Max, Min

from datetime import datetime
from datetime import  date
import calendar
import datetime

@login_required(login_url='/user/login')
def home(request):
    return render_to_response('index_remuneracion.html', context_instance=RequestContext(request))



@login_required(login_url='/user/login')
def pago_empleado(request):
    empleado=Empleados.objects.all()
    contratos = contratacion.objects.exclude(fecha_salida__lte = datetime.datetime.now()).filter(estado = 'ACTIVO')
    return render_to_response('remuneraciones/empleado_pago.html', {'empleados' :empleado, 'contratos':contratos}, context_instance=RequestContext(request))

def descuento_empleado(request):
    empleado=Empleados.objects.all()
    contratos = contratacion.objects.exclude(fecha_salida__lte = datetime.datetime.now()).filter(estado = 'ACTIVO')
    return render_to_response('remuneraciones/empleado_descuento.html', {'empleados' :empleado, 'contratos':contratos}, context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def new_pago(request, cod_emple):
    if request.method == 'POST' :
        formulario = PagosForm(request.POST, request.FILES)
        if formulario.is_valid():
            Pagos.objects.create(
                                    razon = formulario.cleaned_data['razon'],
                                    pago = formulario.cleaned_data['pago'],
                                    descripcion = formulario.cleaned_data['descripcion'],
                                    fecha = datetime.datetime.now(),
                                    empleado_id = cod_emple,
                                   )
            return HttpResponseRedirect('/pago/empleado')
    else:
        formulario = PagosForm()
    return  render_to_response('remuneraciones/new_pago.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@login_required(login_url='/user/login')
def new_descuento(request, cod_emple):
    if request.method == 'POST' :
        formulario = DescuentoForm(request.POST, request.FILES)
        if formulario.is_valid():
            Descuento.objects.create(
                                    razon = formulario.cleaned_data['razon'],
                                    pago = formulario.cleaned_data['pago'],
                                    descripcion = formulario.cleaned_data['descripcion'],
                                    fecha = datetime.datetime.now(),
                                    empleado_id = cod_emple,
                                   )
            return HttpResponseRedirect('/pago/empleado')
    else:
        formulario = DescuentoForm()
    return  render_to_response('remuneraciones/new_descuento.html', {'formulario' :formulario}, context_instance=RequestContext(request))


def planilla_sueldos(request):
    hoy = datetime.datetime.now()
    q45 = contratacion.objects.filter(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO').values('empleado_id')
    empleado = Empleados.objects.filter(id__in = q45)
    contrato = contratacion.objects.filter(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO')
    return render_to_response('remuneraciones/planilla_sueldo.html', {'empleados' :empleado,
                                                                    'contratos':contrato,
                                                }, context_instance=RequestContext(request))


def detalle_planilla(request, id_emple):
    hoy = datetime.datetime.now()
    empleado = get_object_or_404(Empleados, pk=id_emple)
    contrato = contratacion.objects.get(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO', empleado_id = id_emple)
    #q1 = contrato.values('empleado_id')
    descuentos = Descuento.objects.filter(fecha__lte = hoy, fecha__gte=hoy, empleado_id = empleado.id)
    pagos = Pagos.objects.filter(fecha__lte = hoy, fecha__gte=hoy, empleado_id = empleado.id)
    
    q2 = Asistencia.objects.filter(empleado_id = id_emple)
    
    month = hoy.strftime("%m")
    year = hoy.strftime("%Y")
    cal = calendar.Calendar()
    dias = [x for x in cal.itermonthdays(int(year),int(month)) if x][-1]
    lista1 = range(1,dias+1)
    fechas = []
    falta = 0
    retraso = 0
    fin = 0
    for c in lista1:
        fechas +=[date(int(year), int(month), int(c))]
    falta_t = 0
    for f in fechas:
        if f.weekday() == 5 or f.weekday() == 6 :
            fin = fin + 1

    retrasos = q2.filter(obs_m="RETRASO").count()
    retrasos += q2.filter(obs_t="RETRASO").count()
    marcas = q2.filter(fecha__in = fechas).count()
    
    t_descuentos = 0
    t_pagos = 0

    faltas = dias + 1 - fin - marcas
    des_faltas = faltas * contrato.descuento
    retraso = retrasos
    retraso  = retraso/10
    des_retraso = retraso * contrato.descuento

    if pagos:
        t_pag = pagos.aggregate(Sum('pago'))
        t_pago = t_pag.values()
        for p in t_pago:
            t_pagos = p
    else:
        t_pagos = 0.0

    if descuentos :
        t_desc = descuentos.aggregate(Sum('pago'))
        t_descuento = t_desc.values()
        for d in t_descuento:
            t_descuentos = d
    else:
        t_tecuentos = 0.0

    t_descuentos += des_retraso + des_faltas

    total = contrato.sueldo + t_pagos - t_descuentos

    return render_to_response('remuneraciones/detalle_planilla.html',
                                {   'contrato':contrato,
                                    'empleado':empleado,
                                    'descuento':descuentos,
                                    'pago':pagos,
                                    'faltas':faltas,
                                    'des_faltas':des_faltas,
                                    'retrasos':retraso,
                                    'des_retraso':des_retraso,
                                    't_pagos':t_pagos,
                                    't_descuentos':t_descuentos,
                                    'total':total,
                                }, context_instance=RequestContext(request))
