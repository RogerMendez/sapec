#encoding:utf-8
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os
import datetime
from django.conf import settings

from organizacion.models import Unidad, Cargo, Planificacion
from organizacion.form import UnidadForm, CargoForm, PlanificacionForm

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE


def admin_log_addnition(request, objecto, mensaje):
    LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(objecto).pk,
                object_id       = objecto.pk,
                object_repr     = force_unicode(objecto),
                action_flag     = ADDITION,
                change_message = mensaje
            )

def admin_log_change(request, objecto, mensaje):
    LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(objecto).pk,
                object_id       = objecto.pk,
                object_repr     = force_unicode(objecto),
                action_flag     = CHANGE,
                change_message = mensaje
            )

def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    links = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-16")), result, link_callback=links)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


@login_required(login_url="/login")
def index_unidad(request):
    unidades = Unidad.objects.all()
    return render_to_response('unidad/index.html',{'unidades':unidades}, context_instance=RequestContext(request))


@permission_required('organizacion.add_unidad', login_url="/login")
def new_unidad(request):
    if request.method =='POST' :
        formulario = UnidadForm(request.POST, request.FILES)
        if formulario.is_valid() :
            uni = formulario.save()
            messages.add_message(request, messages.INFO, "Se Registro Correctamente la Unidad: " + uni.nombre )
            admin_log_addnition(request, uni, "Creacion De la Unidad")
            return HttpResponseRedirect(reverse(index_unidad))
    else:
        formulario = UnidadForm()
    return render_to_response('unidad/new_unidad.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('organizacion.change_unidad', login_url="/login")
def option_update(request):
    unidades = Unidad.objects.all()
    return render_to_response('unidad/option_update.html',{
        'unidades':unidades,
    },context_instance=RequestContext(request))

@permission_required('organizacion.change_unidad', login_url="/login")
def update_unidad(request, id_unidad):
    unidad = get_object_or_404(Unidad, pk = id_unidad)
    if request.method =='POST' :
        formulario = UnidadForm(request.POST, request.FILES, instance=unidad)
        if formulario.is_valid() :
            uni = formulario.save()
            messages.add_message(request, messages.INFO, "Se Modifico Correctamente la Unidad: <strong>" + uni.nombre + "</strong>")
            admin_log_change(request,uni,"Se Modifico la Unidad")
            return HttpResponseRedirect(reverse(index_unidad))
    else:
        formulario = UnidadForm(instance=unidad)
    return render_to_response('unidad/update_unidad.html', {'formulario' :formulario}, context_instance=RequestContext(request))

@permission_required('organizacion.view_detail_unidad', login_url="/login")
def option_detalle(request):
    unidades = Unidad.objects.all()
    return render_to_response('unidad/option_detalle.html',{
        'unidades':unidades,
    },context_instance=RequestContext(request))

@permission_required('organizacion.view_detail_unidad', login_url="/login")
def detail_unidad(request, id_unidad):
    unidad = get_object_or_404(Unidad, pk = id_unidad)
    return render_to_response('unidad/detail_unidad.html',{
        'unidad':unidad,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.list_unidad_pdf', login_url="/login")
def unidades_pdf(request, pdf):
    unidades = Unidad.objects.all()
    fecha = datetime.datetime.now()
    if not int(pdf):
        return render_to_response('unidad/list_unidades.html',{
            'unidades':unidades,
        }, context_instance=RequestContext(request))
    else:
        html = render_to_string('unidad/list_unidades_pdf.html', {'pagesize':'Letter',
                                                                    'unidades':unidades,
                                                                    'fecha':fecha,
                                                                }, context_instance=RequestContext(request))
        return generar_pdf(html)

@permission_required('organizacion.unidades_sin_cargo', login_url="/login")
def unidades_sin_cargo(request, pdf):
    q1 = Cargo.objects.all().values('unidad_id')
    unidades = Unidad.objects.exclude(id__in = q1)
    if not int(pdf):
        return render_to_response('unidad/unidad_sin_cargo.html',{
            'unidades':unidades,
        }, context_instance=RequestContext(request))
    else:
        html = render_to_string('unidad/unidad_sin_cargo_pdf.html', {'pagesize':'Letter',
                                                                    'unidades':unidades,
                                                                }, context_instance=RequestContext(request))
        return generar_pdf(html)



@login_required(login_url="/login")
def index_cargo(request):
    unidades = Unidad.objects.all()
    return render_to_response('cargo/index.html',{
        'unidades':unidades,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.add_cargo', login_url="/login")
def new_cargo(request):
    if request.method =='POST' :
        formulario = CargoForm(request.POST, request.FILES)
        if formulario.is_valid() :
            cargo = formulario.save()
            unidad = Unidad.objects.get(id = cargo.unidad_id)
            msm = "Se Registro Correctamente el Cargo: <strong>" + cargo.nombre + "</strong> Dentro de la Unidad: <strong>" + unidad.nombre + "</strong>"
            messages.add_message(request, messages.INFO, msm)
            admin_log_addnition(request, cargo, "Creacion De cargo")
            return HttpResponseRedirect(reverse(index_cargo))
    else:
        formulario = CargoForm()
    return render_to_response('cargo/new_cargo.html', {'formulario' :formulario}, context_instance=RequestContext(request))

@permission_required('organizacion.change_cargo', login_url="/login")
def option_update_cargo(request):
    q1 = Cargo.objects.all().values('unidad_id')
    unidades = Unidad.objects.filter(id__in = q1)
    return render_to_response('cargo/option_update.html',{
        'unidades':unidades,
    }, context_instance = RequestContext(request))

@permission_required('organizacion.change_cargo', login_url="/login")
def update_cargo(request, id_cargo):
    cargo = get_object_or_404(Cargo, pk = id_cargo)
    if request.method =='POST' :
        formulario = CargoForm(request.POST, request.FILES, instance=cargo)
        if formulario.is_valid() :
            cargo = formulario.save()
            unidad = Unidad.objects.get(id = cargo.unidad_id)
            msm = "Se Modifico Correctamente el Cargo: <strong>" + cargo.nombre + "</strong> Dentro de la Unidad: <strong>" + unidad.nombre + "</strong>"
            messages.add_message(request, messages.INFO, msm)
            admin_log_change(request, cargo, "Se Modifico el cargo")
            return HttpResponseRedirect(reverse(option_update_cargo))
    else:
        formulario = CargoForm(instance=cargo)
    return render_to_response('cargo/update_cargo.html', {'formulario' :formulario}, context_instance=RequestContext(request))

@permission_required('organizacion.detail_cargo', login_url="/login")
def option_detalle_cargo(request):
    q1 = Cargo.objects.all().values('unidad_id')
    unidades = Unidad.objects.filter(id__in = q1)
    return render_to_response('cargo/option_detalle.html',{
        'unidades':unidades,
    }, context_instance = RequestContext(request))

@permission_required('organizacion.detail_cargo', login_url="/login")
def detalle_cargo(request, id_cargo):
    cargo = get_object_or_404(Cargo, pk = id_cargo)
    return render_to_response('cargo/detalle_cargo.html',{
        'cargo':cargo,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.list_cargos_pdf', login_url="/login")
def cargos_pdf(request, pdf):
    q1 = Cargo.objects.all().values('unidad_id')
    unidades = Unidad.objects.filter(id__in = q1)
    if not int(pdf):
        return render_to_response('cargo/list_cargos.html', {
            'unidades' :unidades,
            }, context_instance=RequestContext(request))
    else:
        html = render_to_string('cargo/list_cargos_pdf.html', {
            'pagesize':'Letter',
            'unidades' :unidades,
        }, context_instance=RequestContext(request))
        return generar_pdf(html)

@login_required(login_url="/login")
def index_planificacion(request):
    planificaciones = Planificacion.objects.all()
    q1 = planificaciones.values('cargo_id')
    cargos = Cargo.objects.filter(id__in = q1)
    return render_to_response('planificacion/index.html', {
        'planificaciones':planificaciones,
        'cargos':cargos,
    }, context_instance=RequestContext(request))


@permission_required('organizacion.add_planificacion', login_url="/login")
def new_planificacion(request):
    if request.method =='POST' :
        formulario = PlanificacionForm(request.POST, request.FILES)
        if formulario.is_valid() :
            plani = formulario.save()
            plani.usuario = request.user
            plani.save()
            msm = "Se Registro Correctamente La Planificación Dentro de: </strong>" + str(plani.cargo) + "<strong>"
            messages.add_message(request, messages.INFO, msm)
            admin_log_addnition(request, plani, "Se Registro La Planificacion")
            return HttpResponseRedirect(reverse(index_planificacion))
    else:
        formulario = PlanificacionForm()
    return render_to_response('planificacion/new_planificacion.html', {'formulario' :formulario}, context_instance=RequestContext(request))

@permission_required('organizacion.change_planificacion', login_url="/login")
def option_update_planificacion(request):
    q1 = Planificacion.objects.all().values('cargo_id')
    cargos = Cargo.objects.filter(id__in = q1)
    return render_to_response('planificacion/option_update.html', {
        'cargos':cargos,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.change_planificacion', login_url="/login")
def update_planificacion(request, id_plani):
    planificacion = get_object_or_404(Planificacion, pk = id_plani)
    if request.method == 'POST' :
        formulario = PlanificacionForm(request.POST, instance = planificacion)
        if formulario.is_valid :
            plani = formulario.save()
            msm = "Se Modifico Correctamente La Planificación Dentro de: </strong>" + str(plani.cargo) + "<strong>"
            messages.add_message(request, messages.INFO, msm)
            admin_log_change(request, plani, "Se Modifico La Planificacion")
            return HttpResponseRedirect(reverse(option_update_planificacion))
    else:
        formulario = PlanificacionForm(instance=planificacion)
    return render_to_response('planificacion/update_planificacion.html',{
        'formulario':formulario,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.detail_planificacion', login_url='/login')
def option_detalle_planificacion(request):
    q1 = Planificacion.objects.all().values('cargo_id')
    cargos = Cargo.objects.filter(id__in = q1)
    return render_to_response('planificacion/option_detalle.html', {
        'cargos':cargos,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.detail_planificacion', login_url='/login')
def detalle_planificacion(request, id_plani):
    planificacion = get_object_or_404(Planificacion, pk = id_plani)
    return render_to_response('planificacion/detalle_planificacion.html',{
        'planificacion':planificacion,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.cancel_planificacion', login_url='/login')
def option_cancel_planificacion(request):
    q1 = Planificacion.objects.all().values('cargo_id')
    cargos = Cargo.objects.filter(id__in = q1)
    return render_to_response('planificacion/option_cancel.html', {
        'cargos':cargos,
    }, context_instance=RequestContext(request))

@permission_required('organizacion.cancel_planificacion', login_url='/login')
def cancel_planificacion(request, id_plani):
    plani = get_object_or_404(Planificacion, pk = id_plani)
    plani.delete()
    msm = "Se Cancelo Correctamente La Planificación Dentro de: </strong>" + str(plani.cargo) + "<strong>"
    messages.add_message(request, messages.INFO, msm)
    return HttpResponseRedirect(reverse(option_cancel_planificacion))

@permission_required("organizacion.plani_cargo", login_url="/login")
def planificaciones_cargos(request):
    q1 = Planificacion.objects.all().values('cargo_id')
    cargos = Cargo.objects.filter(id__in = q1)
    q1 = cargos.values('unidad_id')
    unidades = Unidad.objects.filter(id__in = q1)
    return render_to_response('planificacion/report/seleccion_cargo.html',{
        'cargos' :cargos,
        'unidades' :unidades,
    }, context_instance=RequestContext(request))

@permission_required("organizacion.plani_cargo", login_url="/login")
def planificaciones_cargo(request, id_cargo):
    cargo = get_object_or_404(Cargo, pk = id_cargo)
    planificaciones = Planificacion.objects.filter(cargo = cargo)
    return render_to_response('planificacion/report/planificacion_cargo.html',{
        'cargo' :cargo,
        'planificaciones' :planificaciones,
    }, context_instance = RequestContext(request))