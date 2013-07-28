#encoding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.db.models import Q

from organizacion.models import Unidades, Planificacion, Cargos, Funciones, Conocimiento
from organizacion.forms import UnidadForm, PlanificacionForm, FuncionForm, CargoForm, ConocimientoForm
from personal.models import contratacion
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime, date
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
import datetime



def home(request):
    unidad = Unidades.objects.all()
    return render_to_response('inicio.html', {unidad :unidad}, context_instance=RequestContext(request))


@login_required(login_url='/user/login')
def index_organizacion(request):
    return render_to_response('index_organizacion.html', context_instance=RequestContext(request))


#@login_required(login_url='/user/login')
@permission_required('organizacion.add_unidades', login_url="/user/login")
def nueva_unidad(request):
    if request.method =='POST' :
        formulario = UnidadForm(request.POST, request.FILES)
        if formulario.is_valid() :
            formulario.save()
            return HttpResponseRedirect('/organizacion')
    else:
        formulario = UnidadForm()
    return render_to_response('unidad/new_unidad.html', {'formulario' :formulario}, context_instance=RequestContext(request))

@permission_required('organizacion.option', login_url="/user/login")
def option_unidad(request):
    unidad = Unidades.objects.all()
    return render_to_response('unidad/option_unidad.html', {'unidades' :unidad}, context_instance=RequestContext(request))


#@login_required(login_url='/user/login')
@permission_required('organizacion.change_unidades', login_url="/user/login")
def update_unidad(request, id_unidad):
    unidad = get_object_or_404(Unidades, pk = id_unidad)
    #Unidades = request.nombre
    if request.method == 'POST':
        formulario = UnidadForm(request.POST, instance = unidad)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/unidad/option')
    else:
        formulario = UnidadForm(instance = unidad)
    return render_to_response('unidad/update_unidad.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@login_required(login_url='/user/login')
def cargo_plani(request, id_cargo):
    planificacion = Planificacion.objects.filter(cargo_id = id_cargo)
    q1 = Cargos.objects.get(id = id_cargo)
    funciones = Funciones.objects.filter(cargo_id = id_cargo)
    conocimiento = Conocimiento.objects.filter(cargo_id = id_cargo)
    return render_to_response('unidad/unid_plani.html',{'planificacion' :planificacion,
                                                        'cargo' :q1,
                                                        'conocimientos' :conocimiento,
                                                        'funciones':funciones}
        , context_instance=RequestContext(request))


#PLANIFICACION
#@login_required(login_url='/user/login')
@permission_required('organizacion.add_planificacion', login_url="/user/login")
def nueva_plani(request):
    if request.method =='POST' :
        formulario = PlanificacionForm(request.POST, request.FILES)
        if formulario.is_valid() :
            formulario.save()
            return HttpResponseRedirect('/organizacion')
    else:
        formulario = PlanificacionForm()
    return render_to_response('unidad/new_plani.html', {'formulario' :formulario}, context_instance=RequestContext(request))


#@login_required(login_url='/user/login')
@permission_required('organizacion.option_plani', login_url="/user/login")
def option_plani(request):
    q2 = Planificacion.objects.filter(estado = True, cantidad__gt=0).values('cargo_id')
    planificacion = Planificacion.objects.all()
    cargos = Cargos.objects.filter(id__in = q2)
    return render_to_response('unidad/option_plani.html',{'planificaciones' :planificacion, 'cargos' :cargos}, context_instance=RequestContext(request))


@permission_required('organizacion.change_planificacion', login_url="/user/login")
def update_planificacion(request, id_plani):
    planificacion = get_object_or_404(Planificacion, pk = id_plani)
    #Unidades = request.nombre
    if request.method == 'POST':
        formulario = PlanificacionForm(request.POST, instance = planificacion)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/planificacion/option')
    else:
        formulario = PlanificacionForm(instance = planificacion)
    return render_to_response('unidad/update_plani.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('organizacion.delete_planificacion', login_url="/user/login")
def cancel_plani(request, id_plani):
    planificacion = Planificacion.objects.get(id = id_plani)
    planificacion.delete()
    #planificacion.save()
    return HttpResponseRedirect('/planificacion/option')


#CARGO

@permission_required('organizacion.add_cargos', login_url="/user/login")
def new_cargo(request):
    if request.method =='POST' :
        formulario = CargoForm(request.POST, request.FILES)
        if formulario.is_valid() :
            formulario.save()
            return HttpResponseRedirect('/organizacion')
    else:
        formulario = CargoForm()
    return render_to_response('cargo/new_cargo.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('organizacion.option_cargo', login_url="/user/login")
def option_cargo(request):
    cargo = Cargos.objects.all()
    q1 = cargo.distinct().values('unidad_id')
    unidad = Unidades.objects.filter(id__in = q1)
    return render_to_response('cargo/option_cargo.html', {'cargos' :cargo, 'unidades' :unidad}, context_instance=RequestContext(request))


@permission_required('organizacion.change_cargos', login_url="/user/login")
def update_cargo(request, id_cargo):
    cargo = get_object_or_404(Cargos, pk = id_cargo)
    if request.method == 'POST':
        formulario = CargoForm(request.POST, instance = cargo)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/cargo/option')
    else:
        formulario = CargoForm(instance = cargo)
    return render_to_response('cargo/update_cargo.html', {'formulario' :formulario}, context_instance=RequestContext(request))



#FUNCIONES

@permission_required('organizacion.add_funciones', login_url="/user/login")
def new_funcion(request):
    if request.method == 'POST' :
        formulario = FuncionForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/organizacion')
    else:
        formulario = FuncionForm()
    return  render_to_response('cargo/new_funcion.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('organizacion.option_funcion', login_url="/user/login")
def option_function(request):
    q1 = Funciones.objects.filter(estado = True).values('cargo_id')
    funcion = Funciones.objects.filter()
    cargo = Cargos.objects.filter(id__in = q1)
    q2 = cargo.values('unidad_id')
    unidad = Unidades.objects.filter(id__in = q2)
    return render_to_response('cargo/option_funcion.html', {'funciones' :funcion, 'unidades' :unidad, 'cargos' :cargo}, context_instance=RequestContext(request) )


@permission_required('organizacion.change_funciones', login_url="/user/login")
def update_funcion(request, id_funcion):
    funcion = get_object_or_404(Funciones, pk = id_funcion)
    if request.method == 'POST':
        formulario = FuncionForm(request.POST, instance=funcion)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/funcion/option')
    else:
        formulario = FuncionForm(instance=funcion)
    return render_to_response('cargo/update_funcion.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('organizacion.delete_funciones', login_url="/user/login")
def delete_funcion(request, id_funcion):
    funcion = Funciones.objects.get(pk = id_funcion)
    funcion.delete()
    return HttpResponseRedirect('/funcion/option')


#CONOCIMIENTO
@permission_required('organizacion.add_conocimiento', login_url="/user/login")
def new_conocimiento(request):
    if request.method == 'POST' :
        formulario = ConocimientoForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/organizacion')
    else:
        formulario = ConocimientoForm()
    return  render_to_response('cargo/new_conocimiento.html', {'formulario' :formulario}, context_instance=RequestContext(request))

@permission_required('organizacion.option_conoci', login_url="/user/login")
def option_conocimiento(request):
    conocimiento = Conocimiento.objects.filter(estado = True)
    q2 = conocimiento.values('cargo_id')
    cargo = Cargos.objects.filter(id__in = q2)
    q2 = cargo.values('unidad_id')
    unidad = Unidades.objects.filter(id__in = q2)
    return render_to_response('cargo/option_conocimiento.html', {'conocimientos' :conocimiento, 'unidades' :unidad, 'cargos' :cargo}, context_instance=RequestContext(request) )

@permission_required('organizacion.change_conocimiento', login_url="/user/login")
def update_conocimiento(request, cono_id):
    cono = get_object_or_404(Conocimiento, pk = cono_id)
    if request.method == 'POST':
        formulario = ConocimientoForm(request.POST, instance=cono)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/conocimiento/option')
    else:
        formulario = ConocimientoForm(instance=cono)
    return render_to_response('cargo/update_conocimiento.html', {'formulario' :formulario}, context_instance=RequestContext(request))

@permission_required('organizacion.delete_conocimiento', login_url="/user/login")
def delete_conocimiento(request, cono_id):
    cono = get_object_or_404(Conocimiento, pk = cono_id)
    cono.delete()
    return HttpResponseRedirect('/conocimiento/option')


def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-16")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


@permission_required('organizacion.list_unidades', login_url="/user/login")
def unidad_pdf(request, pdf = None):
    unidades=Unidades.objects.all()
    if pdf == "1" :
        html = render_to_string('unidad/reporte_unidades_pdf.html', {'pagesize':'Letter', 'unidades' :unidades, }, context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return render_to_response('unidad/reporte_unidades.html', {'unidades' :unidades, }, context_instance=RequestContext(request))


def cargos_pdf(request, pdf=None):
    cargos = Cargos.objects.all()
    unidades = Unidades.objects.all()
    if pdf == "1":
        html = render_to_string('cargo/reporte_cargos_pdf.html', {'pagesize':'Letter', 'unidades' :unidades, 'cargos' :cargos }, context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return render_to_response('cargo/reporte_cargos_existentes.html', {'unidades' :unidades, "cargos" :cargos }, context_instance=RequestContext(request))

def cargos_no_empleado(request, pdf = None) :
    hoy = date.today()
    q1 = contratacion.objects.filter(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO')
    q2 = q1.values('cargo_id').distinct()
    cargos = Cargos.objects.exclude(id__in = q2)
    if pdf == "1":
        html = render_to_string('cargo/cargo_no_empleado_pdf.html', {'pagesize':'Letter', 'cargos' :cargos }, context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return render_to_response('cargo/cargo_no_empleado.html', {'cargos' :cargos }, context_instance=RequestContext(request))


def seleccion_cargos_cono(request):
    q2 = Conocimiento.objects.filter(estado = True).values('cargo_id')
    q3 = Funciones.objects.filter(estado = True).values('cargo_id')
    q3 = Cargos.objects.filter(
        Q(id__in =q2)|Q(id__in=q3)
    )
    q1 = Cargos.objects.all()
    return render_to_response('cargo/seleccion_cargo_cono.html', {"cargos" :q3 }, context_instance=RequestContext(request))


def conocimiento_funciones(request, cargo_id):
    q1 = get_object_or_404(Cargos, pk = cargo_id)
    q2 = Conocimiento.objects.filter(cargo_id = q1.id)
    q3 = Funciones.objects.filter(cargo_id = q1.id)
    return render_to_response('cargo/conocimiento_funciones.html', {
                                                                "cargo" :q1,
                                                                'conocimientos':q2,
                                                                'funciones':q3,
                                                                    }, context_instance=RequestContext(request))

def view_planificaciones_cargo(request):
    q2 = Planificacion.objects.filter(estado = True, cantidad__gt=0).values('cargo_id')
    q1 = Cargos.objects.filter(id__in = q2)
    return render_to_response('cargo/seleccion_planificacion_cargo.html',{
                                                                    'cargos':q1,
                                                                    }, context_instance=RequestContext(request))

def planificacion_cargo(request, id_cargo):
    q1 = get_object_or_404(Cargos, pk = id_cargo)
    q2 = Planificacion.objects.filter(cargo_id = id_cargo, estado = True)
    return render_to_response('cargo/planificacion_cargo.html',{'cargo':q1, 'planificaciones':q2}, context_instance=RequestContext(request))
