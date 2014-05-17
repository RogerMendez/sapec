# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from django import template
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os
from django.db.models import Sum, Count
import datetime
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from contratacion.models import Contratacion, Movilidad, Terminar
from contratacion.form import PersonaSearchForm
from organizacion.models import Cargo, Unidad
from personal.models import Persona
from models import Pagos, Descuentos
from form import PagosForm, DescuentosForm, FechasPlanillaForm
from asistencia.models import Asistencia

register = template.Library()

def admin_log_addnition(request, objecto, mensaje):
    LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(objecto).pk,
                object_id       = objecto.pk,
                object_repr     = force_unicode(objecto),
                action_flag     = ADDITION,
                change_message = mensaje,
            )

def admin_log_change(request, objecto, mensaje):
    LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(objecto).pk,
                object_id       = objecto.pk,
                object_repr     = force_unicode(objecto),
                action_flag     = CHANGE,
                change_message = mensaje,
            )

@login_required(login_url="/login")
def index_remuneracion(request):
    hoy = datetime.datetime.now()
    personas = Persona.objects.all()
    opagos = Pagos.objects.filter(fecha = hoy)
    descuentos = Descuentos.objects.filter(fecha = hoy)
    return render_to_response('remuneraciones/index.html', {
        'personas':personas,
        'opagos':opagos,
        'descuentos':descuentos,
    }, context_instance=RequestContext(request))

@login_required(login_url="/login")
def otros_pagos(request):
    hoy = datetime.datetime.now()
    if request.method == "GET":
        formulario = PersonaSearchForm(request.GET)
        if formulario.is_valid():
            texto = formulario.cleaned_data['texto']
            per = Persona.objects.all()
            personas = per.filter(
                Q(nombre__icontains = texto)|Q(paterno__icontains = texto)|Q(materno__icontains = texto)|Q(ci__icontains = texto)
            )
            contratos = Contratacion.objects.filter(fecha_entrada__lte = hoy, fecha_salida__gte = hoy, estado=True, persona = personas)
            return render_to_response('remuneraciones/otros_pagos.html',{
                'contratos':contratos,
                'formulario':formulario,
            }, context_instance = RequestContext(request))
    else:
        formulario = PersonaSearchForm()
        contratos = Contratacion.objects.filter(fecha_entrada__lte = hoy, fecha_salida__gte = hoy, estado=True)
    return render_to_response('remuneraciones/otros_pagos.html',{
        'contratos':contratos,
        'formulario':formulario,
    }, context_instance = RequestContext(request))

@permission_required('remuneraciones.add_pagos', login_url="/login")
def select_persona_pagos(request):
    fecha_actual = datetime.datetime.now()
    fecha = date.today()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('remuneraciones/select_persona_pago.html',{
        'contrataciones':contrataciones,
        'personas':personas,
        'fecha_actual':fecha,
    }, context_instance=RequestContext(request))


@permission_required('remuneraciones.add_pagos', login_url="/login")
def new_pago(request, id_contrato):
    contrato = get_object_or_404(Contratacion, pk = id_contrato)
    if request.method == 'POST':
        formulario = PagosForm(request.POST)
        if formulario.is_valid():
            pago = formulario.save()
            pago.contrato = contrato
            pago.usuario = request.user
            pago.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente el Pago para: <strong>%s</strong>' %(contrato.persona) )
            admin_log_addnition(request, pago, 'Pago Creado')
            return HttpResponseRedirect(reverse(otros_pagos))
    else:
        formulario = PagosForm()
    return render_to_response('remuneraciones/new_pago.html', {
        'formulario':formulario,
    }, context_instance = RequestContext(request))

@login_required(login_url="/login")
def descuentos_index(request):
    hoy = datetime.datetime.now()
    if request.method == "GET":
        formulario = PersonaSearchForm(request.GET)
        if formulario.is_valid():
            texto = formulario.cleaned_data['texto']
            per = Persona.objects.all()
            personas = per.filter(
                Q(nombre__icontains = texto)|Q(paterno__icontains = texto)|Q(materno__icontains = texto)|Q(ci__icontains = texto)
            )
            contratos = Contratacion.objects.filter(fecha_entrada__lte = hoy, fecha_salida__gte = hoy, estado=True, persona = personas)
            return render_to_response('remuneraciones/descuentos.html',{
                'contratos':contratos,
                'formulario':formulario,
            }, context_instance = RequestContext(request))
    else:
        formulario = PersonaSearchForm()
        contratos = Contratacion.objects.filter(fecha_entrada__lte = hoy, fecha_salida__gte = hoy, estado=True)
    return render_to_response('remuneraciones/descuentos.html',{
        'contratos':contratos,
        'formulario':formulario,
    }, context_instance = RequestContext(request))

@permission_required('remuneraciones.add_descuentos', login_url="/login")
def select_persona_descuentos(request):
    fecha_actual = datetime.datetime.now()
    fecha = date.today()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('remuneraciones/select_persona_descuento.html',{
        'contrataciones':contrataciones,
        'personas':personas,
        'fecha_actual':fecha,
    }, context_instance=RequestContext(request))

@permission_required('remuneraciones.add_descuentos', login_url="/login")
def new_descuento(request, id_contrato):
    contrato = get_object_or_404(Contratacion, pk = id_contrato)
    if request.method == "POST":
        formulario = DescuentosForm(request.POST)
        if formulario.is_valid():
            descuento = formulario.save()
            descuento.contrato = contrato
            descuento.usuario = request.user
            descuento.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente el Descuento para: <strong>%s</strong>' %(contrato.persona) )
            admin_log_addnition(request, descuento, 'Descuento Creado')
            return HttpResponseRedirect(reverse(descuentos_index))
    else:
        formulario = DescuentosForm()
    return render_to_response('remuneraciones/new_descuento.html', {
        'formulario':formulario,
    }, context_instance = RequestContext(request))


def planilla_sueldos(request):
    fecha = datetime.datetime.now()
    q2 = descuentos = asistencias = pagos = None
    formulario = FechasPlanillaForm(request.GET or None)
    if formulario.is_valid():
        mes = int(formulario.cleaned_data['mes'])
        anho = int(formulario.cleaned_data['anho'])
        fecha = date(anho, mes, 2)
        q2 = contratos = Contratacion.objects.all()
        for con in contratos:
            anho_ent = con.fecha_entrada.strftime("%Y")
            anho_sal = con.fecha_salida.strftime("%Y")
            if int(anho_ent) > anho:
                q2 = q2.exclude(id = con.id)
            if int(anho_sal) < anho :
                q2 = q2.exclude(id = con.id)
            mes_ent = con.fecha_entrada.strftime("%m")
            mes_sal = con.fecha_salida.strftime("%m")
            if int(mes_ent) > mes and int(anho_ent) == anho :
                q2 = q2.exclude(id = con.id)
            if int(mes_sal) < mes and int(anho_sal) == anho:
                q2 = q2.exclude(id = con.id)

        descuentos = Descuentos.objects.filter(contrato_id__in = q2.values('id'), fecha__year = anho, fecha__month = mes)
        descuentos = descuentos.values('contrato_id').annotate(sum_monto = Sum('monto'))
        pagos = Pagos.objects.filter(contrato_id__in = q2.values('id'), fecha__year = anho, fecha__month = mes)
        pagos = pagos.values('contrato_id').annotate(sum_pago = Sum('pago'))
        asistencia = Asistencia.objects.filter(persona_id__in = q2.values('persona_id'), fecha__year = anho, fecha__month = mes)
        asistencias = asistencia.values('persona_id').annotate(sum_asistencia = Count('fecha'))
        #personas = Persona.objects.all()
    return render_to_response('remuneraciones/planilla_sueldos.html',{
        'contratos':q2,
        'fecha':fecha,
        'formulario':formulario,
        'descuentos':descuentos,
        'pagos':pagos,
        'asistencias':asistencias,
        #'suma':suma,
    }, context_instance=RequestContext(request))