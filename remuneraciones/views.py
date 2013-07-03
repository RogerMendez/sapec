from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from personal.models import Empleados, contratacion
from remuneraciones.models import Pagos, Descuento
from remuneraciones.form import PagosForm, DescuentoForm

from django.contrib.auth.decorators import login_required

from datetime import datetime

@login_required(login_url='/user/login')
def home(request):
    return render_to_response('index_remuneracion.html', context_instance=RequestContext(request))



@login_required(login_url='/user/login')
def pago_empleado(request):
    empleado=Empleados.objects.all()
    contratos = contratacion.objects.exclude(fecha_salida__lte = datetime.today()).filter(estado = 'ACTIVO')
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
                                    fecha = datetime.today(),
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
                                    fecha = datetime.today(),
                                    empleado_id = cod_emple,
                                   )
            return HttpResponseRedirect('/pago/empleado')
    else:
        formulario = DescuentoForm()
    return  render_to_response('remuneraciones/new_pago.html', {'formulario' :formulario}, context_instance=RequestContext(request))