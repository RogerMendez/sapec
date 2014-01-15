# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os
import datetime
from django.conf import settings
from personal.models import Persona, Estudios, OtrosEstudios, Experiencias
from personal.form import PersonaForm, EstudiosForm, OtrosEstudiosForm, ExperienciasForm

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

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

def index_personal(request):
    persona = Persona.objects.get(usuario = request.user)
    return render_to_response('personal/index.html',{
        'persona':persona,

    }, context_instance = RequestContext(request))

@permission_required('personal.show_datos_persona', login_url="/login")
def show_datos_persona(request):
    persona = Persona.objects.get(usuario = request.user)
    return render_to_response('personal/datos_persona.html',{
        'per' :persona,
    }, context_instance=RequestContext(request))

@permission_required('personal.change_persona', login_url="/login")
def completar_datos_persona(request):
    persona = Persona.objects.get(usuario = request.user)
    if request.method == 'POST':
        formulario = PersonaForm(request.POST, request.FILES, instance=persona)
        if formulario.is_valid():
            per = formulario.save()
            per.completo = True
            per.save()
            messages.add_message(request, messages.INFO, "Se Registro Correctamente los Datos Sr(a): %s %s %s" % (per.nombre, per.paterno,   per.materno) )
            admin_log_change(request, per, 'Modifico los Datos de Persona')
            return HttpResponseRedirect(reverse(index_personal))
    else:
        formulario = PersonaForm(instance=persona)
    return render_to_response('personal/completar_persona.html',{
        'formulario':formulario,
    }, context_instance = RequestContext(request))


@permission_required("personal.show_estudios_persona", login_url="/login")
def show_estudios(request):
    persona = Persona.objects.get(usuario = request.user)
    estudios = Estudios.objects.filter(persona = persona)
    return render_to_response('personal/show_estudios.html', {
        'estudios':estudios,
    }, context_instance = RequestContext(request))


@permission_required('personal.add_persona')
def new_estudio(request):
    fecha = datetime.datetime.now()
    if request.method == "POST":
        formulario = EstudiosForm(request.POST)
        if formulario.is_valid():
            estu = formulario.save()
            persona = Persona.objects.get(usuario = request.user)
            estu.persona = persona
            estu.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente los Datos Del Estudio En la Institución: <strong>%s</strong>' %estu.institucion )
            admin_log_addnition(request, estu, 'Estudio Creado')
            return HttpResponseRedirect(reverse(show_estudios))
    else:
        formulario = EstudiosForm()
    return render_to_response('personal/new_estudio.html', {
        'formulario':formulario,
        'fecha_actual':fecha,
    }, context_instance = RequestContext(request))


@permission_required("personal.change_persona", login_url="/login")
def update_estudio(request, id_estudio):
    estudio = get_object_or_404(Estudios, pk = id_estudio)
    fecha = datetime.datetime.now()
    if request.method == "POST":
        formulario = EstudiosForm(request.POST, instance=estudio)
        if formulario.is_valid():
            estu = formulario.save()
            messages.add_message(request, messages.INFO, u'Se Modifico Correctamente los Datos Del Estudio En la Institución: <strong>%s</strong>' %estu.institucion )
            admin_log_change(request, estu, 'Estudio Modificado')
            return HttpResponseRedirect(reverse(show_estudios))
    else:
        formulario = EstudiosForm(instance=estudio)
    return render_to_response('personal/update_estudio.html', {
        'formulario':formulario,
        'fecha_actual':fecha,
    }, context_instance = RequestContext(request))

@permission_required('personal.delete_persona', login_url="/login")
def delete_estudio(request, id_estudio):
    estudio = get_object_or_404(Estudios, pk = id_estudio)
    estudio.delete()
    messages.add_message(request, messages.INFO, u'Se Elimino el Estudio En la Institución: <strong>%s</strong>' %estudio.institucion )
    return HttpResponseRedirect(reverse(show_estudios))

@permission_required("personal.show_otrosestudios_persona", login_url="/login")
def show_otros_estudios(request):
    persona = Persona.objects.get(usuario = request.user)
    otrosestudios = OtrosEstudios.objects.filter(persona = persona)
    return render_to_response('personal/show_otrosestudios.html', {
        'otrosestudios':otrosestudios,
    }, context_instance = RequestContext(request))

@permission_required("personal.add_otrosestudios", login_url="/login")
def new_otro_estudio(request):
    fecha_actual = datetime.datetime.now()
    if request.method == "POST":
        formulario = OtrosEstudiosForm(request.POST)
        if formulario.is_valid():
            estu = formulario.save()
            persona = Persona.objects.get(usuario = request.user)
            estu.persona = persona
            estu.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente los Datos Del Curso/Conferencia: <strong>%s</strong>' %estu.curso )
            admin_log_addnition(request, estu, 'Estudio Creado')
            return HttpResponseRedirect(reverse(show_otros_estudios))
    else:
        formulario = OtrosEstudiosForm()
    return render_to_response('personal/new_otro_estudio.html', {
        'formulario':formulario,
        'fecha_actual':fecha_actual,
    }, context_instance = RequestContext(request))

@permission_required("personal.change_otrosestudios", login_url="/login")
def update_otro_estudio(request, id_oestudio):
    fecha_actual = datetime.datetime.now()
    oestudio = get_object_or_404(OtrosEstudios, pk = id_oestudio)
    if request.method == "POST":
        formulario = OtrosEstudiosForm(request.POST, instance=oestudio)
        if formulario.is_valid():
            estu = formulario.save()
            messages.add_message(request, messages.INFO, u'Se Modifico Correctamente los Datos Del Curso/Conferencia: <strong>%s</strong>' %estu.curso )
            admin_log_change(request, estu, 'Estudio Modificado')
            return HttpResponseRedirect(reverse(show_otros_estudios))
    else:
        formulario = OtrosEstudiosForm(instance=oestudio)
    return render_to_response('personal/update_otro_estudio.html', {
        'formulario':formulario,
        'fecha_actual':fecha_actual,
    }, context_instance = RequestContext(request))

@permission_required("personal.delete_otrosestudios", login_url="/login")
def delete_otro_estudio(request, id_oestudio):
    oestudio = get_object_or_404(OtrosEstudios, pk = id_oestudio)
    oestudio.delete()
    messages.add_message(request, messages.INFO, u'Se Elimino Correctamente los Datos Del Curso/Conferencia: <strong>%s</strong>' %oestudio.curso )
    return HttpResponseRedirect(reverse(show_otros_estudios))