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
from datetime import date, timedelta, datetime, time
#import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from contratacion.models import Contratacion
from personal.models import Persona
from models import Asistencia, Permiso
from form import AsistenciaForm, FechasForm, PermisoForm


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

def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    links = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-16")), result, link_callback=links)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def restar_horas(hora1, hora2):
    #hora1 - hora2
    h1 = int(hora1[0:2])
    h2 = int(hora2[0:2])
    m1 = int(hora1[3:5])
    m2 = int(hora2[3:5])
    h = h1 - h2
    m  = m1 - m2
    if m < 0:
        m = m + 60
        h -= 1
    if m < 10:
        min = "0" + str(m)
    else:
        min = str(m)
    if h < 10 :
        hr = "0" + str(h)
    else:
        hr = str(h)
    return str(hr) + ":" + str(min)

def sumar_horas(hora1, hora2):
    h1 = int(hora1[0:2])
    h2 = int(hora2[0:2])
    m1 = int(hora1[3:5])
    m2 = int(hora2[3:5])
    h = h1 + h2
    m  = m1 + m2
    if m >= 60:
        m = m - 60
        h += 1
    if m < 10:
        min = "0" + str(m)
    else:
        min = str(m)
    if h < 10 :
        hr = "0" + str(h)
    else:
        hr = str(h)
    return str(hr) + ":" + str(min)


def index_asistencia(request):
    hoy = datetime.now()
    hora1 = hoy.strftime("%H:%M")
    hora = hora1#sumar_horas(hora1, "30:10")
    h = int(hora1[0:2])
    m = int(hora1[3:5])
    return render_to_response('asistencia/index_asistencia.html',{
        'hora':hora,
        'hr':h,
        'min':m,
    }, context_instance = RequestContext(request))

#@permission_required('asistencia.add_asistencia', login_url="/login")
def new_asistencia(request):
    msm = ""
    if request.method == "POST":
        formulario = AsistenciaForm(request.POST)
        if formulario.is_valid():
            ci = formulario.cleaned_data['ci']
            if Persona.objects.filter(ci = ci):
                persona = Persona.objects.get(ci = ci)
                hoy = datetime.now()
                if Contratacion.objects.filter(estado = True, fecha_salida__gte = hoy, persona = persona):
                    if Asistencia.objects.filter(persona = persona, fecha = hoy):
                        asistencia = Asistencia.objects.get(persona = persona, fecha = hoy)
                        #admin_log_change(request, asistencia, 'Modifico los Datos de Persona')
                    else:
                        asistencia = Asistencia.objects.create(
                            persona = persona,
                        )
                    hora = hoy.strftime("%H:%M")
                    if hora >= "22:01" or hora <= "05:59" :
                            msm = 'Sr(a) <strong>%s %s, %s<strong> <p class="lead">No Esta Dentro del Horario Para su Registro de Asistencia<p>' %(persona.materno, persona.paterno, persona.nombre)
                    else:

                        if hora >= "06:00" and hora <= "08:15" and asistencia.entrada_m == None:
                            asistencia.entrada_m = hora
                            asistencia.save()
                            msm = "Registro de Asistencia Exitosa</br>Entrada Mañana"
                        elif hora >= "13:00" and hora <= "14:15" and asistencia.entrada_t == None:
                            asistencia.entrada_t = hora
                            asistencia.save()
                            msm = "Registro de Asistencia Exitosa</br>Entrada Tarde"
                        elif hora >= "12:00" and hora <= "12:59" and asistencia.salida_m == None :
                            asistencia.salida_m = hora
                            asistencia.save()
                            msm = "Registro de Asistencia Exitosa</br>Salida Mañana"
                        elif hora >= "18:00" and hora <= "22:00" and asistencia.salida_t == None :
                            asistencia.salida_t = hora
                            asistencia.save()
                            msm = "Registro de Asistencia Exitosa</br>Salida Tarde"
                        else:
                            #msm = "EN HORARIO TARDE"
                            if hora >= "08:16" and hora <= "11:59" and asistencia.entrada_m == None :
                                #entrada mañana tarde
                                asistencia.entrada_m = hora
                                if  asistencia.atraso == None:
                                    atraso = "00:00"
                                else:
                                    atraso = str(asistencia.atraso)
                                asistencia.atraso = sumar_horas(atraso, restar_horas(hora, "08:16"))
                                asistencia.save()
                                msm = "Registro Exitoso Con un retraso de: %s" %asistencia.atraso
                            elif hora >= "14:16" and hora <= "17:59" and asistencia.entrada_t == None :
                                #Entrada tarde retraso
                                if  asistencia.atraso == None:
                                    atraso = "00:00"
                                else:
                                    atraso = str(asistencia.atraso)
                                asistencia.entrada_t = hora
                                asistencia.atraso = sumar_horas(atraso, restar_horas(hora, "14:16"))
                                asistencia.save()
                                msm = "Registro de Asistencia Exitosa</br>Entrada Tarde Con Retraso"
                            else:
                                msm = "Usted Ya registro su asistencia"
                else:
                    msm = "Usted No Cuenta Con un Contrato Vigente"
            else:
                msm = "Usted no Esta Registrado en el Sistema"
            messages.add_message(request, messages.INFO, msm )
            return HttpResponseRedirect("/")
    else:
        formulario = AsistenciaForm()
    return render_to_response('asistencia/new_asistencia.html', {
        'formulario':formulario,
    }, context_instance=RequestContext(request))

@permission_required("asistencia.detail_asistencia", login_url="/login")
def personal_asistencia(request):
    fecha_actual = datetime.now()
    fecha = date.today()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('asistencia/list_empleado_asistencia.html',{
        'contrataciones':contrataciones,
        'personas':personas,
        'fecha_actual':fecha,
    }, context_instance=RequestContext(request))

@permission_required("asistencia.detail_asistencia", login_url="/login")
def seleccion_fechas_detalle(request, id_persona):
    persona = get_object_or_404(Persona, pk = id_persona)
    hoy = datetime.now()
    contrato = Contratacion.objects.get(estado = True, fecha_salida__gte = hoy, persona = persona)
    if request.method == 'POST' :
        formulario = FechasForm(request.POST)
        if formulario.is_valid():
            fecha_ini = request.POST['fecha_ini']
            fecha_fin = request.POST['fecha_fin']
            anho_ini = datetime.strptime(fecha_ini, "%d/%m/%Y").strftime("%Y")
            mes_ini = datetime.strptime(fecha_ini, "%d/%m/%Y").strftime("%m")
            dia_ini = datetime.strptime(fecha_ini, "%d/%m/%Y").strftime("%d")
            anho_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").strftime("%Y")
            mes_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").strftime("%m")
            dia_fin = datetime.strptime(fecha_fin, "%d/%m/%Y").strftime("%d")
            return HttpResponseRedirect(reverse(detalle_asistencia, args=(persona.id, dia_ini, mes_ini, anho_ini, dia_fin, mes_fin, anho_fin, 0,)))
    else:
        formulario = FechasForm()
    return  render_to_response('asistencia/seleccion_fechas_detail.html', {
        'formulario' :formulario,
        'contrato':contrato,
    }, context_instance=RequestContext(request))

@permission_required("asistencia.detail_asistencia", login_url="/login")
def detalle_asistencia(request, id_persona, dia_ini, mes_ini, anho_ini, dia_fin, mes_fin, anho_fin, pdf):
    hoy = datetime.now()
    fecha_ini =  date(int(anho_ini), int(mes_ini), int(dia_ini))
    fecha_fin = date(int(anho_fin), int(mes_fin), int(dia_fin))
    flag = True
    fechas = []
    d = fecha_ini
    fechas+=[d]
    while flag:
        d=d+timedelta(days=1)
        fechas+=[d]
        if d >= fecha_fin :
            flag = False

    persona = get_object_or_404(Persona, pk = id_persona)
    contrato = Contratacion.objects.get(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO', persona = persona)
    asistencia = Asistencia.objects.filter(persona = persona, fecha__gte = contrato.fecha_entrada)
    if  int(pdf) :
        html = render_to_string('asistencia/detalle_asistencia_pdf.html', {
            'pagesize':'Letter',
            'mes' :fechas,
            'empleado':persona,
            'asistencia':asistencia,
        }, context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return render_to_response('asistencia/detail_asistencia.html',{
            'mes' :fechas,
            'cod_emple':id_persona,
            'fecha_ini':fecha_ini,
            'fecha_fin':fecha_fin,
            'persona':persona,
            'asistencia':asistencia,
        }, context_instance = RequestContext(request))


def index_permiso(request):
    hoy = datetime.now()
    permisos = Permiso.objects.all()
    return render_to_response('permiso/index.html', {
        'permisos':permisos,
    }, context_instance=RequestContext(request))

@permission_required('asistencia.add_permiso', login_url="/login")
def select_persona_permiso(request):
    fecha_actual =  datetime.now()
    contrataciones = Contratacion.objects.filter(estado = True, fecha_salida__gte = fecha_actual)
    q1 = contrataciones.values('persona_id')
    personas = Persona.objects.filter(id__in = q1)
    return render_to_response('permiso/select_persona_permiso.html',{
        'contrataciones':contrataciones,
        'personas':personas,
    }, context_instance=RequestContext(request))

@permission_required('asistencia.add_permiso', login_url="/login")
def new_permiso(request, id_persona):
    fecha_actual = datetime.now()
    persona = get_object_or_404(Persona, pk = id_persona)
    if request.method == "POST":
        formulario = PermisoForm(request.POST)
        if formulario.is_valid():
            #hora = hoy.strftime("%H:%M")
            ini = formulario.cleaned_data['inicio']
            fin = formulario.cleaned_data['finalizacion']
            fecha = formulario.cleaned_data['fecha_permiso']
            permiso = formulario.save()
            permiso.persona = persona
            permiso.usuario = request.user
            permiso.save()
            if Asistencia.objects.filter(persona=persona, fecha = fecha):
                asistencia = Asistencia.objects.get(persona=persona, fecha = fecha)
            else:
                asistencia = Asistencia.objects.create(
                            persona = persona,
                        )
            asistencia.fecha = fecha
            if ini <= time(8,00,00):
                asistencia.entrada_m = "08:00"
            elif fin >= time(12,00,00) and ini <= time(12,00,00) :
                asistencia.salida_m = "12:00"
            elif ini <= time(14,00,00) and fin >= time(14,00,00) :
                asistencia.entrada_t = "14:00"
            elif fin >= time(18,00,00) and ini <= time(18,00,00):
                asistencia.salida_t = "18:00"
            asistencia.save()
            messages.add_message(request, messages.INFO, "Permiso Registrado Correctamente Para el Sr(a): %s %s %s Para la Fecha %s %s - %s - %s" % (persona.nombre, persona.paterno, persona.materno, permiso.fecha_permiso, ini, fin, asistencia.persona) )
            admin_log_addnition(request, permiso, 'Permiso Creado')
            return HttpResponseRedirect(reverse(select_persona_permiso))
    else:
        formulario = PermisoForm()
    return render_to_response('permiso/new_permiso.html', {
        'formulario':formulario,
        'fecha_actual':fecha_actual,
    }, context_instance=RequestContext(request))