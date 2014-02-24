# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os
import datetime
from datetime import date
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from models import Contratacion, Movilidad, Terminar
from form import PersonaSearchForm, ContratacionEventualForm, RazonCambioForm, TerminarContratoForm, PersonaForm
from organizacion.models import Cargo, Unidad
from personal.models import Persona
from users.views import code_activation_create
from users.form import EmailForm


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

@permission_required('contratacion.show_contrato', login_url="/login")
def show_contrataciones(request):
    fecha_actual = datetime.datetime.now()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('contratacion/show_contrataciones.html',{
        'contrataciones':contrataciones,
        'personas':personas,
    }, context_instance=RequestContext(request))

@permission_required('contratacion.add_contratacion', login_url="/login")
def select_cargo(request):
    q1 = Cargo.objects.all().values('unidad_id')
    unidades = Unidad.objects.filter(id__in = q1)
    return render_to_response('contratacion/select_cargo.html', {
        'unidades':unidades,
    }, context_instance=RequestContext(request))

@permission_required('contratacion.add_contratacion', login_url="/login")
def select_persona(request, id_cargo):
    cargo = get_object_or_404(Cargo, pk = id_cargo)
    fecha = datetime.datetime.now()
    q1 = Contratacion.objects.filter(
            Q(fecha_entrada__lte = fecha, fecha_salida__gte = fecha)|Q(estado = True)|Q(permanente = True)
            )
    q2 = q1.values('persona_id')
    personas = Persona.objects.exclude(id__in = q2)
    if request.method == "GET":
        formulario = PersonaSearchForm(request.GET)
        if formulario.is_valid():
            per = Persona.objects.exclude(id__in = q2)
            texto = formulario.cleaned_data['texto']
            personas = per.filter(
                Q(nombre__contains = texto)|Q(paterno__contains = texto)|Q(materno__contains = texto)|Q(ci__contains = texto)
            )
            return render_to_response('contratacion/select_persona.html',{
                'cargo':cargo,
                'personas':personas,
                'formulario':formulario,
            }, context_instance = RequestContext(request))
    else:
        formulario = PersonaSearchForm()
        personas = Persona.objects.exclude(id__in = q2)
    return render_to_response('contratacion/select_persona.html',{
        'cargo':cargo,
        'personas':personas,
        'formulario':formulario,
    }, context_instance = RequestContext(request))

@permission_required('contratacion.add_contratacion', login_url="/login")
def new_persona(request, id_cargo):
    hoy = datetime.datetime.now()
    cargo = get_object_or_404(Cargo, pk = id_cargo)
    if request.method == 'POST' :
        formulario = PersonaForm(request.POST, request.FILES)
        foremail = EmailForm(request.POST)
        if formulario.is_valid() and foremail.is_valid() :
            persona = formulario.save()
            carnet = formulario.cleaned_data['ci']
            email = foremail.cleaned_data['email']
            usuario = User.objects.create_user(carnet, email, carnet)
            usuario.is_active = False
            usuario.save()
            persona.usuario = usuario
            code = code_activation_create()
            persona.code_activation = code
            persona.completo = True
            persona.save()
            subject = 'Confirmacion De Correo Electronico'
            text_content = 'Mensaje...nLinea 2nLinea3'
            html_content = '<h2>Confirmacion de Correo</h2><p>Haga click en el siguiente Enlace</p><p><a href="http://127.0.0.1:8000/user/confirmar/?code='+code+'">Confirmar Cuenta</a></p></br><p>El Nombre de Usuario y Contraseña es su Cedula de Identidad</p>'
            from_email = '"SAPEC" <sieboliva@gmail.com>'
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            msm = "Persona Creada Correctamentebr><h5>Un Mensaje fue enviado al correo de la persona para Activar su Cuenta</h5>"
            messages.add_message(request, messages.INFO, msm)
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente A la Persona: <strong>%s %s, %s</strong>' %(persona.paterno, persona.materno, persona.nombre))
            admin_log_addnition(request, persona, 'Persona Registrada')
            return HttpResponseRedirect(reverse(new_contrato, args=(cargo.id, persona.id, )))
    else:
        formulario = PersonaForm()
        foremail = EmailForm()
    return render_to_response('contratacion/new_persona.html', {
        'formulario' :formulario,
        'foremail' :foremail,
        'cargo' :cargo,
        'hoy' :hoy,
    }, context_instance=RequestContext(request))

@permission_required('contratacion.add_contratacion', login_url="/login")
def new_contrato(request, id_cargo, id_persona):
    fecha = datetime.datetime.now()
    cargo = get_object_or_404(Cargo, pk = id_cargo)
    persona = get_object_or_404(Persona, pk = id_persona)
    if request.method == "POST":
        formulario = ContratacionEventualForm(request.POST)
        if formulario.is_valid():
            contra = formulario.save()
            contra.persona = persona
            contra.cargo = cargo
            contra.usuario = request.user
            contra.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente el Contrato de: <strong>%s %s, %s</strong>' %(persona.paterno, persona.materno, persona.nombre) )
            admin_log_addnition(request, contra, 'Contrato Creado')
            return HttpResponseRedirect(reverse(show_contrataciones))
    else:
        formulario = ContratacionEventualForm()
    return render_to_response('contratacion/new_contrato.html',{
        'cargo':cargo,
        'persona':persona,
        'formulario':formulario,
        'fecha_actual':fecha,
    }, context_instance = RequestContext(request))

@permission_required('contratacion.view_contrato', login_url="/login")
def list_contratos_informacion(request):
    fecha_actual = datetime.datetime.now()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('contratacion/list_contratos_informacion.html',{
        'contrataciones':contrataciones,
        'personas':personas,
    }, context_instance=RequestContext(request))

@permission_required('contratacion.view_contrato', login_url="/login")
def view_contrato(request, id_persona):
    fecha_actual = datetime.datetime.now()
    persona = get_object_or_404(Persona, pk = id_persona)
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    contrato = contrataciones.get(persona_id = persona.id)
    cargo = Cargo.objects.get(pk = contrato.cargo_id)
    unidad = Unidad.objects.get(cargo = cargo )
    unidad.descripcion = unidad.descripcion[0 : 200] + '...'
    cargo.descripcion = cargo.descripcion[0 : 200] + '...'
    return render_to_response('contratacion/view_contrato.html', {
        'persona':persona,
        'contrato':contrato,
        'cargo':cargo,
        'unidad':unidad,
    }, context_instance=RequestContext(request))


@permission_required("contratacion.add_movilidad", login_url="/login")
def list_contratos_movilidad(request):
    fecha_actual = datetime.datetime.now()
    fecha = date.today()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('contratacion/list_contratos_movilidad.html',{
        'contrataciones':contrataciones,
        'personas':personas,
        'fecha_actual':fecha,
    }, context_instance=RequestContext(request))

@permission_required("contratacion.add_movilidad", login_url="/login")
def select_cargo_cambio(request, id_contrato):
    contrato = get_object_or_404(Contratacion, pk = id_contrato)
    q1 = Cargo.objects.all()
    q2 = q1.values('unidad_id')
    unidades = Unidad.objects.filter(id__in = q2)
    return render_to_response('contratacion/select_cargo_cambio.html', {
        'unidades':unidades,
        'contrato':contrato,
    }, context_instance=RequestContext(request))

@permission_required("contratacion.add_movilidad", login_url="/login")
def new_cambio(request, id_cargo, id_contrato):
    cargo = get_object_or_404(Cargo, pk = id_cargo)
    contrato = get_object_or_404(Contratacion, pk = id_contrato)
    if request.method == "POST":
        formulario = RazonCambioForm(request.POST)
        if formulario.is_valid():
            cambio = formulario.save()
            cambio.cargo = cargo
            cambio.contrato = contrato
            cambio.save()
            Contratacion.objects.create(
                                fecha_entrada = datetime.datetime.now(),
                                fecha_salida = contrato.fecha_salida,
                                estado = 'ACTIVO',
                                sueldo = contrato.sueldo,
                                descuento = contrato.descuento,
                                persona = contrato.persona,
                                cargo = cargo,
                                usuario = request.user
                                )
            contrato.estado = False
            contrato.fecha_salida = datetime.datetime.now()
            contrato.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente el Cambio de Puesto de <strong>%s</strong> A <strong>%s - %s</strong>' %(contrato.cargo, cargo.unidad, cargo.nombre) )
            admin_log_change(request, contrato, 'Contrato Modificado')
            admin_log_addnition(request, cambio, 'Cambio Realizado')
            return HttpResponseRedirect(reverse(list_contratos_movilidad))
    else:
        formulario = RazonCambioForm()
    return render_to_response('contratacion/new_razon_cambio.html', {
        'formulario':formulario,
        'contrato':contrato,
    }, context_instance=RequestContext(request))

@permission_required("contratacion.add_terminar", login_url="/login")
def list_contratos_terminar(request):
    fecha_actual = datetime.datetime.now()
    fecha = date.today()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('contratacion/list_contratos_terminar.html',{
        'contrataciones':contrataciones,
        'personas':personas,
        'fecha_actual':fecha,
    }, context_instance=RequestContext(request))

@permission_required("contratacion.add_terminar", login_url="/login")
def terminar_contrato(request, id_contrato):
    contrato = get_object_or_404(Contratacion, pk = id_contrato)
    if request.method == "POST":
        formulario = TerminarContratoForm(request.POST)
        if formulario.is_valid():
            persona = Persona.objects.get(id = contrato.persona_id)
            terminar = formulario.save()
            terminar.contrato_id = contrato.id
            terminar.usuario = request.user
            terminar.save()
            contrato.estado = False
            contrato.fecha_salida = datetime.datetime.now()
            contrato.save()
            messages.add_message(request, messages.INFO, u'Se Termino Correctamente el Contrato <strong>%s %s, %s</strong> ' %(persona.paterno, persona.materno, persona.nombre))
            admin_log_addnition(request, terminar, "Contrato Terminado")
            admin_log_change(request, contrato, 'Contrato Modificado')
            return HttpResponseRedirect(reverse(list_contratos_terminar))
    else:
        formulario = TerminarContratoForm()
    return render_to_response('contratacion/new_terminar_contrato.html', {
        'formulario':formulario,
        'contrato':contrato,
    }, context_instance = RequestContext(request))





