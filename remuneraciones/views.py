#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from personal.models import Empleados, contratacion, Asistencia
from remuneraciones.models import Pagos, Descuento
from remuneraciones.form import PagosForm, DescuentoForm

from django.contrib.auth.decorators import login_required

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
    return  render_to_response('remuneraciones/new_pago.html', {'formulario' :formulario}, context_instance=RequestContext(request))


def planilla_sueldos(request):
    sueldos = []
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
    lista = []
    month = hoy.strftime("%m")
    year = hoy.strftime("%Y")
    cal = calendar.Calendar()
    dias = [x for x in cal.itermonthdays(int(year),int(month)) if x][-1]
    lista1 = range(1,dias+1)
    fechas = []
    falta = 0
    retraso = 0
    for c in lista1:
        fechas +=[date(int(year), int(month), int(c))]
    for f in fechas:
        if f.weekday() != 5 and f.weekday() != 6 :
            if q2.filter(fecha = f).count() < 4:
                falta = falta + 1
            if q2.filter(fecha = f, obs = 'RETRASO').count():
                retraso = retraso + 1
    lista +=[falta]
    lista +=[falta * contrato.descuento]
    lista +=[retraso]
    retraso  = retraso % 10
    lista +=[retraso * contrato.descuento]
    return render_to_response('remuneraciones/detalle_planilla.html',
                                {   'contrato':contrato,
                                    'empleado':empleado,
                                    'descuento':descuentos,
                                    'pago':pagos,
                                    'lista':lista,
                                }, context_instance=RequestContext(request))
