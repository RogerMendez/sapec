#encoding:utf-8
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os
import datetime
from datetime import date
from django.conf import settings
from personal.models import Persona, Estudios, OtrosEstudios, Experiencias, Idiomas, Observacion
from personal.form import PersonaForm, EstudiosForm, OtrosEstudiosForm, ExperienciasForm, IdiomasForm, ObservacionForm
from contratacion.models import Contratacion, Movilidad
from contratacion.form import PersonaSearchForm
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

@login_required(login_url="/login")
def index_personal(request):
    persona = Persona.objects.get(usuario = request.user)
    estudios = Estudios.objects.filter(persona = persona)
    otrosestudios = OtrosEstudios.objects.filter(persona = persona)
    experiencias = Experiencias.objects.filter(persona = persona)
    idiomas = Idiomas.objects.filter(persona = persona)
    return render_to_response('personal/index.html',{
        'persona':persona,
        'estudios':estudios,
        'otrosestudios':otrosestudios,
        'experiencias':experiencias,
        'idiomas':idiomas,
    }, context_instance = RequestContext(request))

@login_required(login_url="/login")
def show_datos_persona(request):
    persona = Persona.objects.get(usuario = request.user)
    return render_to_response('personal/datos_persona.html',{
        'per' :persona,
    }, context_instance=RequestContext(request))

@login_required(login_url="/login")
def completar_datos_persona(request):
    persona = Persona.objects.get(usuario = request.user)
    fecha = datetime.datetime.now()
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
        'fecha_actual':fecha,
    }, context_instance = RequestContext(request))


@login_required(login_url="/login")
def show_estudios(request):
    persona = Persona.objects.get(usuario = request.user)
    estudios = Estudios.objects.filter(persona = persona)
    return render_to_response('personal/show_estudios.html', {
        'estudios':estudios,
    }, context_instance = RequestContext(request))


@login_required(login_url="/login")
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


@login_required(login_url="/login")
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

@login_required(login_url="/login")
def delete_estudio(request, id_estudio):
    estudio = get_object_or_404(Estudios, pk = id_estudio)
    estudio.delete()
    messages.add_message(request, messages.INFO, u'Se Elimino el Estudio En la Institución: <strong>%s</strong>' %estudio.institucion )
    return HttpResponseRedirect(reverse(show_estudios))

@login_required(login_url="/login")
def show_otros_estudios(request):
    persona = Persona.objects.get(usuario = request.user)
    otrosestudios = OtrosEstudios.objects.filter(persona = persona)
    return render_to_response('personal/show_otrosestudios.html', {
        'otrosestudios':otrosestudios,
    }, context_instance = RequestContext(request))

@login_required(login_url="/login")
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

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def delete_otro_estudio(request, id_oestudio):
    oestudio = get_object_or_404(OtrosEstudios, pk = id_oestudio)
    oestudio.delete()
    messages.add_message(request, messages.INFO, u'Se Elimino Correctamente los Datos Del Curso/Conferencia: <strong>%s</strong>' %oestudio.curso )
    return HttpResponseRedirect(reverse(show_otros_estudios))

@login_required(login_url="/login")
def show_experiencias_trabajo(request):
    persona = Persona.objects.get(usuario = request.user)
    experiencias = Experiencias.objects.filter(persona = persona)
    return render_to_response('personal/show_experiencias_trabajo.html', {
        'experiencias' :experiencias,
    }, context_instance = RequestContext(request))

@login_required(login_url="/login")
def new_experiencia(request):
    fecha_actual = datetime.datetime.now()
    if request.method == "POST":
        formulario = ExperienciasForm(request.POST)
        if formulario.is_valid():
            experiencia = formulario.save()
            persona = Persona.objects.get(usuario = request.user)
            experiencia.persona = persona
            experiencia.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente la Experiencia de Trabajo en: <strong>%s</strong>' %experiencia.institucion )
            admin_log_addnition(request, experiencia, 'Experiencia Creada')
            return HttpResponseRedirect(reverse(show_experiencias_trabajo))
    else:
        formulario = ExperienciasForm()
    return render_to_response('personal/new_experiencia_trabajo.html', {
        'formulario':formulario,
        'fecha_actual':fecha_actual,
    }, context_instance = RequestContext(request))

@login_required(login_url="/login")
def update_experiencia_trabajo(request, id_experiencia):
    texperienia = get_object_or_404(Experiencias, pk = id_experiencia)
    fecha_actual = datetime.datetime.now()
    if request.method == "POST":
        formulario = ExperienciasForm(request.POST, instance=texperienia)
        if formulario.is_valid():
            experiencia = formulario.save()
            messages.add_message(request, messages.INFO, u'Se Modifico Correctamente la Experiencia de Trabajo en: <strong>%s</strong>' %experiencia.institucion )
            admin_log_change(request, experiencia, 'Experiencia Modificada')
            return HttpResponseRedirect(reverse(show_experiencias_trabajo))
    else:
        formulario = ExperienciasForm(instance=texperienia)
    return render_to_response('personal/update_experiencia_trabajo.html', {
        'formulario':formulario,
        'fecha_actual':fecha_actual,
    }, context_instance = RequestContext(request))

@login_required(login_url="/login")
def delete_experiencia_trabajo(request, id_experiencia):
    experiencia = get_object_or_404(Experiencias, pk = id_experiencia)
    experiencia.delete()
    messages.add_message(request, messages.INFO, u'Se Elimino Correctamente la Experiencia de Trabajo: <strong>%s</strong>' %experiencia.institucion )
    return HttpResponseRedirect(reverse(show_experiencias_trabajo))

@login_required(login_url="/login")
def show_idiomas(request):
    persona = Persona.objects.get(usuario = request.user)
    idiomas = Idiomas.objects.filter(persona = persona)
    return render_to_response('personal/show_idiomas.html',{
        'idiomas':idiomas,
    }, context_instance = RequestContext(request))

@login_required(login_url="/login")
def new_idioma(request):
    if request.method == "POST":
        formulario = IdiomasForm(request.POST)
        if formulario.is_valid():
            idioma = formulario.save()
            persona = Persona.objects.get(usuario = request.user)
            idioma.persona = persona
            idioma.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente el Idioma: <strong>%s</strong>' %idioma.idioma )
            admin_log_addnition(request, idioma, 'Idioma Creado')
            return HttpResponseRedirect(reverse(show_idiomas))
    else:
        formulario = IdiomasForm()
    return render_to_response('personal/new_idioma.html',{
        'formulario':formulario,
    }, context_instance=RequestContext(request))


@login_required(login_url="/login")
def update_idioma(request, id_idioma):
    idioma = get_object_or_404(Idiomas, pk = id_idioma)
    if request.method == "POST":
            formulario = IdiomasForm(request.POST, instance=idioma)
            if formulario.is_valid():
                idioma = formulario.save()
                messages.add_message(request, messages.INFO, u'Se Modifico Correctamente el Idioma: <strong>%s</strong>' %idioma.idioma )
                admin_log_change(request, idioma, 'Idioma Modificado')
                return HttpResponseRedirect(reverse(show_idiomas))
    else:
        formulario = IdiomasForm(instance=idioma)
    return render_to_response('personal/update_idioma.html',{
        'formulario':formulario,
    }, context_instance=RequestContext(request))

@login_required(login_url="/login")
def delete_idioma(request, id_idioma):
    idioma = get_object_or_404(Idiomas, pk = id_idioma)
    idioma.delete()
    messages.add_message(request, messages.INFO, u'Se Elimino Correctamente el Idioma: <strong>%s</strong>' %idioma.idioma )
    return HttpResponseRedirect(reverse(show_idiomas))

@permission_required('personal.show_tarjetas_qr_persona', login_url="/login")
def select_personal_qr(request):
    fecha_actual = datetime.datetime.now()
    fecha = date.today()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('personal/list_empleado_qr.html',{
        'contrataciones':contrataciones,
        'personas':personas,
        'fecha_actual':fecha,
    }, context_instance=RequestContext(request))

@permission_required('personal.show_tarjetas_qr_persona', login_url="/login")
def tarjeta_qr(request, id_persona):
    persona = get_object_or_404(Persona, pk = id_persona)
    direccion = "http://192.168.43.117:90/asistencia/qr/?code="+str(persona.ci)
    return render_to_response('personal/tarjeta_qr.html', {
        'persona' :persona,
        'direccion' :direccion
    }, context_instance=RequestContext(request))

@login_required(login_url="/login")
def my_tarjeta_qr(request):
    persona = Persona.objects.get(usuario = request.user)
    direccion = "http://192.168.43.117:90/asistencia/qr/?code="+str(persona.ci)
    return render_to_response('personal/tarjeta_qr.html', {
        'persona' :persona,
        'direccion' :direccion
    }, context_instance=RequestContext(request))

@permission_required('personal.view_kardex_persona', login_url="/login")
def select_personal_kardex(request):
    if request.method == "GET":
        formulario = PersonaSearchForm(request.GET)
        if formulario.is_valid():
            texto = formulario.cleaned_data['texto']
            per = Persona.objects.all()
            personas = per.filter(
                Q(nombre__icontains = texto)|Q(paterno__icontains = texto)|Q(materno__icontains = texto)|Q(ci__icontains = texto)
            )
            return render_to_response('personal/select_persona_kardex.html',{
                'personas':personas,
                'formulario':formulario,
            }, context_instance = RequestContext(request))
    else:
        formulario = PersonaSearchForm()
        personas = Persona.objects.all()
    return render_to_response('personal/select_persona_kardex.html',{
        'personas':personas,
        'formulario':formulario,
    }, context_instance = RequestContext(request))

@permission_required('personal.view_kardex_persona', login_url="/login")
def view_kardex(request, id_persona):
    persona = get_object_or_404(Persona, pk = id_persona)
    estudios = Estudios.objects.filter(persona = persona)
    otrosestudios = OtrosEstudios.objects.filter(persona = persona)
    experiencias = Experiencias.objects.filter(persona = persona)
    idiomas = Idiomas.objects.filter(persona = persona)
    return render_to_response('personal/view_kardex_persona.html',{
        'persona':persona,
        'estudios':estudios,
        'otrosestudios':otrosestudios,
        'experiencias':experiencias,
        'idiomas':idiomas,
    }, context_instance = RequestContext(request))

@permission_required('personal.view_kardex_empresa_persona', login_url="/login")
def select_personal_kardex_empresa(request):
    if request.method == "GET":
        formulario = PersonaSearchForm(request.GET)
        if formulario.is_valid():
            texto = formulario.cleaned_data['texto']
            per = Persona.objects.all()
            personas = per.filter(
                Q(nombre__icontains = texto)|Q(paterno__icontains = texto)|Q(materno__icontains = texto)|Q(ci__icontains = texto)
            )
            return render_to_response('personal/select_persona_kardex_empresa.html',{
                'personas':personas,
                'formulario':formulario,
            }, context_instance = RequestContext(request))
    else:
        formulario = PersonaSearchForm()
        personas = Persona.objects.all()
    return render_to_response('personal/select_persona_kardex_empresa.html',{
        'personas':personas,
        'formulario':formulario,
    }, context_instance = RequestContext(request))

@permission_required('personal.view_kardex_empresa_persona', login_url="/login")
def view_kardex_persona_empresa(request, id_persona):
    q1 = get_object_or_404(Persona, pk=id_persona)
    q2 = Contratacion.objects.filter(persona = q1)
    q5 = Movilidad.objects.filter(contrato_id__in = q2.values('id'))
    #q3 = Cargo.objects.filter()
    q4 = Observacion.objects.filter(persona = q1)
    return render_to_response('personal/view_kardex_persona_empresa.html', {
                                'persona':q1,
                                'contratos':q2,
                                'movilidad':q5,
                                'observaciones':q4,
                            }, context_instance=RequestContext(request))


@login_required(login_url="/login")
def index_observaciones(request):
    hoy = datetime.datetime.now()
    observaciones = Observacion.objects.filter(fecha = hoy)
    return render_to_response('observaciones/index.html', {
        'observaciones':observaciones,
    }, context_instance=RequestContext(request))

@permission_required('personal.add_observacion', login_url="/login")
def select_persona_observacion(request):
    fecha_actual = datetime.datetime.now()
    fecha = date.today()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('observaciones/select_empleado_observacion.html',{
        'personas':personas,
    }, context_instance=RequestContext(request))

@permission_required('personal.add_observacion', login_url="/login")
def new_observacion(request, id_persona):
    persona = get_object_or_404(Persona, pk = id_persona)
    if request.method == "POST":
        formulario = ObservacionForm(request.POST)
        if formulario.is_valid():
            obs = formulario.save()
            obs.usuario = request.user
            obs.persona = persona
            obs.save()
            messages.add_message(request, messages.INFO, u'Se Registro Correctamente La Observacion Para %s %s, %s: ' %(persona.paterno, persona.materno, persona.nombre))
            admin_log_addnition(request, obs, 'Observacion Creada')
            return HttpResponseRedirect(reverse(select_persona_observacion))
    else:
        formulario = ObservacionForm()
    return render_to_response('observaciones/new_observacion.html', {
        'formulario':formulario,
    }, context_instance = RequestContext(request))

@permission_required('personal.list_observaciones', login_url="/login")
def list_observaciones(request):
    if request.method == "GET":
        formulario = PersonaSearchForm(request.GET)
        if formulario.is_valid():
            texto = formulario.cleaned_data['texto']
            per = Persona.objects.all()
            personas = per.filter(
                Q(nombre__icontains = texto)|Q(paterno__icontains = texto)|Q(materno__icontains = texto)|Q(ci__icontains = texto)
            )
            return render_to_response('observaciones/list_observaciones.html',{
                'personas':personas,
                'formulario':formulario,
            }, context_instance = RequestContext(request))
    else:
        formulario = PersonaSearchForm()
        personas = Persona.objects.all()
    return render_to_response('observaciones/list_observaciones.html',{
        'personas':personas,
        'formulario':formulario,
    }, context_instance = RequestContext(request))
