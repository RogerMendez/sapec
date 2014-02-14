# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os
import datetime
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from contratacion.models import Contratacion, Movilidad, Terminar
from organizacion.models import Cargo, Unidad
from personal.models import Persona
from models import Pagos, Descuentos
from form import PagosForm, DescuentosForm


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

def index_remuneracion(request):
    personas = Persona.objects.all()
    return render_to_response('remuneraciones/index.html', {
        'personas':personas,
    }, context_instance=RequestContext(request))


def otros_pagos(request):
    pagos = Pagos.objects.all()
    return render_to_response('remuneraciones/otros_pagos.html', {
        'pagos':pagos,
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








def descuentos_index(request):
    descuentos = Descuentos.objects.all()
    return render_to_response('remuneraciones/descuentos.html', {
        'descuentos':descuentos,
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


