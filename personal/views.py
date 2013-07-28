#encoding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

from organizacion.models import Unidades, Cargos, Funciones
from personal.form import EmpleadoForm, ProfesionForm, Contrato, AsistenciaForm, ObservacionForm, PermisoForm, FechasForm, AsistenciaFormEdid
from personal.models import Empleados, contratacion, Asistencia, Observacion, Permiso, moviidad


from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, AdminPasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required

from django.conf import settings

from datetime import datetime, time
from datetime import  date, timedelta
import datetime

import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
import os



@login_required(login_url='/user/login')
def home(request):
    return render_to_response('index_personal.html', context_instance=RequestContext(request))


#@login_required(login_url='/user/login')
@permission_required('personal.add_empleados', login_url="/user/login")
def new_empleado(request, cod_cargo):
    #cargo = Cargos.objects.filter(id = cod_cargo)
    cargo = Cargos.objects.get(pk = cod_cargo)
    if request.method == 'POST' :
        formulario = EmpleadoForm(request.POST, request.FILES)
        if formulario.is_valid() :
            carnet = formulario.cleaned_data['ci']
            nombre = formulario.cleaned_data['nombre']
            paterno = formulario.cleaned_data['paterno']
            email = formulario.cleaned_data['email']
            emple = Empleados.objects.filter(ci = carnet)
            if(emple):
                return HttpResponseRedirect('/contrato/new/'+str(carnet)+"/"+str(cod_cargo)+"/")
            else:
                newuser = User.objects.create_user(carnet, email, carnet)
                formulario.save()
                per = Empleados.objects.get(ci = carnet)
                per.usuario_id=newuser.id
                per.save()
                newuser.is_active = 0
                newuser.first_name = nombre
                newuser.last_name = paterno
                newuser.save()
                #formulario.save()
                return HttpResponseRedirect('/contrato/new/'+str(carnet)+"/"+str(cod_cargo)+"/")
    else:
        formulario = EmpleadoForm()
    return render_to_response('personal/new_empleado.html', {'formulario' :formulario, 'cargo' :cargo}, context_instance=RequestContext(request))


@permission_required('personal.option_empleados', login_url="/user/login")
def option_empleado(request):
    hoy = datetime.datetime.now()
    empleado=Empleados.objects.all()
    contratos = contratacion.objects.filter(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO')
    return render_to_response('personal/option_empleado_permiso.html', {'empleados' :empleado, 'contratos':contratos}, context_instance=RequestContext(request))


@permission_required('personal.option_update_empleados', login_url="/user/login")
def option_update_empleado(request):
    hoy = datetime.datetime.now()
    empleado=Empleados.objects.all()
    #contratos = contratacion.objects.filter(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO')
    return render_to_response('personal/option_empleado_update.html', {'empleados' :empleado}, context_instance=RequestContext(request))


@permission_required('personal.option_contrato_empleados', login_url="/user/login")
def view_contratacion(request):
    hoy = datetime.datetime.now()
    empleado=Empleados.objects.all()
    contratos = contratacion.objects.filter(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO')
    return render_to_response('personal/view_contrato_empleado.html', {'empleados' :empleado, 'contratos':contratos}, context_instance=RequestContext(request))

@permission_required('personal.option_observacion_empleados', login_url="/user/login")
def registro_observacion_observacion(request):
    hoy = datetime.datetime.now()
    empleado=Empleados.objects.all()
    contratos = contratacion.objects.filter(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO')
    return render_to_response('personal/view_registro_observacion.html', {'empleados' :empleado, 'contratos':contratos}, context_instance=RequestContext(request))    


@permission_required('personal.change_empleados', login_url="/user/login")
def update_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleados, pk = empleado_id)
    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST, request.FILES, instance = empleado)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/personal/option/update')
    else:
        formulario = EmpleadoForm(instance = empleado)
    return render_to_response('personal/update_empleado.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('personal.add_profesion', login_url="/user/login")
def new_profesion(request):
    if request.method == 'POST' :
        formulario = ProfesionForm(request.POST, request.FILES)
        if formulario.is_valid() :
            formulario.save()
            return HttpResponseRedirect('/personal')
    else:
        formulario = ProfesionForm()
    return render_to_response('personal/new_profesion.html', {'formulario' :formulario}, context_instance=RequestContext(request))


#CONTRATACION

@permission_required('personal.list_cargos_unidad', login_url="/user/login")
def cargos_contrato(request):
    cargo = Cargos.objects.all()
    q1 = cargo.values('unidad_id')
    unidad = Unidades.objects.filter(id__in = q1)
    return render_to_response('personal/cargo_contrato.html', {'cargos' :cargo, 'unidades' :unidad}, context_instance=RequestContext(request))


@permission_required('personal.add_contratacion', login_url="/user/login")
def new_contrato(request, empleado_ci, cargo_id):
    cargo = Cargos.objects.get(pk = cargo_id)
    empleado = Empleados.objects.get(ci = empleado_ci)
    if request.method == 'POST' :
        formulario = Contrato(request.POST, request.FILES)
        if formulario.is_valid() :
            empleado = Empleados.objects.get(ci=int(empleado_ci))
            id =empleado.id
            fecha_fin =formulario.cleaned_data['fecha_fin']
            sueldo=formulario.cleaned_data['sueldo']
            descuento=formulario.cleaned_data['descuento']
            cargo=int(cargo_id)
            c = contratacion.objects.create(fecha_entrada=datetime.datetime.now(),
                                        fecha_salida=fecha_fin,
                                        estado='ACTIVO',
                                        sueldo=sueldo,
                                        descuento=descuento,
                                        empleado_id=id,
                                        cargo_id=cargo,
                                        )
            return HttpResponseRedirect('/contrato/show/'+str(c.id)+'/'+str(0)+'/')
    else:
        formulario = Contrato()
    return render_to_response('personal/new_contratacion.html', {'formulario' :formulario, 'empleado_ci':empleado_ci, 'cargo' :cargo, 'empleado' :empleado}, context_instance=RequestContext(request))



@permission_required('personal.view_contratacion', login_url="/user/login")
def show_contrato(request, cod_contrato, pdf = 0) :
    contrato = get_object_or_404(contratacion, pk = cod_contrato)
    cargo = Cargos.objects.get( pk = contrato.cargo_id)
    unidad = Unidades.objects.get(pk = cargo.unidad_id)
    funciones = Funciones.objects.filter(cargo_id = cargo.id)
    unidad.descripcion = unidad.descripcion[0 : 100] + '...'
    cargo.descripcion = cargo.descripcion[0 : 100] + '...'
    empleado = Empleados.objects.get(pk = contrato.empleado_id)
    if int(pdf) :
        html = render_to_string('personal/show_contrato_pdf.html', {'pagesize':'Letter',
                                                                'cargo' :cargo,
                                                                'unidad' :unidad,
                                                                'contrato' :contrato,
                                                                'empleado' :empleado,
                                                                'funciones' :funciones},
                                context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return render_to_response('personal/show_contrato.html', {'cargo' :cargo,
                                                                  'unidad' :unidad,
                                                                  'contrato' :contrato,
                                                                  'empleado' :empleado,
                                                                  'funciones' :funciones},
                                  context_instance=RequestContext(request))



def new_asistencia(request):
    if request.method == 'POST' :
        formulario = AsistenciaForm(request.POST, request.FILES)
        if formulario.is_valid() :
            carnet = formulario.cleaned_data['ci']
            emple = Empleados.objects.get(ci = carnet)
            hoy = datetime.datetime.now()
            if Empleados.objects.filter(ci = carnet) and contratacion.objects.filter(fecha_entrada__lte = hoy, fecha_salida__gte = hoy, estado='ACTIVO', empleado__ci__exact = carnet ):

                cod_emple = emple.id
                if Asistencia.objects.filter(empleado_id = cod_emple, fecha = hoy):
                    q1 = Asistencia.objects.get(fecha = hoy, empleado_id = cod_emple)
                else:
                    Asistencia.objects.create(
                                                fecha = hoy,
                                                empleado_id = cod_emple,
                                            )
                    q1 = Asistencia.objects.get(fecha = hoy, empleado_id = cod_emple)

                hora = hoy.strftime("%H:%M")
                #Modificar las Horas
                if hora >= "06:00" and hora <= "08:15" :
                    #Entrada mañana
                    if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_m__lte = "08:15", entrada_m__gte = "06:00") :
                        q1.entrada_m = hora
                        q1.save()
                elif hora >= "13:00" and hora <= "14:15" :
                    #"Entrada Tarde"
                    if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_t__lte = "14:15", entrada_t__gte = "13:00") :
                        q1.entrada_t = hora
                        q1.save()
                elif hora >= "12:00" and hora <= "12:59" :
                    #salida mañana
                    if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, salida_m__lte = "12:59", salida_m__gte = "12:00") :
                        q1.salida_m = hora
                        q1.save()
                elif hora >= "18:00" and hora <= "22:00" :
                    #salida tarde
                    if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, salida_t__lte = "22:00", salida_t__gte = "18:00") :
                        q1.salida_t = hora
                        q1.save()
                else:
                    if hora >= "08:16" and hora <= "11:59" :
                        #entrada mañana tarde
                        if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_m__lte = "11:59", entrada_m__gte = "08:16") :
                            q1.entrada_m = hora
                            q1.obs_m = 'RETRASO'
                            q1.save()
                    if hora >= "14:16" and hora <= "17:59" :
                        #Entrada tarde retraso
                        if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_t__lte = "17:59", entrada_t__gte = "14:16") :
                            q1.entrada_t = hora
                            q1.obs_t = 'RETRASO'
                            q1.save()
                    if hora >= "22:01" and hora <= "05:59" :
                        return HttpResponseRedirect('/personal/')
            else:
                return HttpResponseRedirect('/view/kardex/'+str(emple.id)+'/')
            return HttpResponseRedirect('/view/kardex/'+str(emple.id)+'/')
    else:
        formulario = AsistenciaForm()
    return  render_to_response('personal/new_asistencia.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('personal.asistencia_qr', login_url="/user/login")
def asistecia(request, ci_emple):
    carnet = ci_emple
    hoy = datetime.datetime.now()
    emple = Empleados.objects.get(ci = carnet)
    if Empleados.objects.filter(ci = carnet) and contratacion.objects.filter(fecha_entrada__lte = hoy, fecha_salida__gte = hoy, estado='ACTIVO', empleado__ci__exact = carnet ):
        emple = Empleados.objects.get(ci = carnet)
        cod_emple = emple.id
        hora = hoy.strftime("%H:%M")
        #Modificar las Horas
        if Asistencia.objects.filter(empleado_id = cod_emple, fecha = hoy):
            q1 = Asistencia.objects.get(fecha = hoy, empleado_id = cod_emple)
        else:
            Asistencia.objects.create(
                                        fecha = hoy,
                                        empleado_id = cod_emple,
                                    )
            q1 = Asistencia.objects.get(fecha = hoy, empleado_id = cod_emple)

        #Modificar las Horas
        if hora >= "06:00" and hora <= "08:15" :
            #Entrada mañana
            if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_m__lte = "08:15", entrada_m__gte = "06:00") :
                q1.entrada_m = hora
                q1.save()
        elif hora >= "13:00" and hora <= "14:15" :
            #"Entrada Tarde"
            if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_t__lte = "14:15", entrada_t__gte = "13:00") :
                q1.entrada_t = hora
                q1.save()
        elif hora >= "12:00" and hora <= "12:59" :
            #salida mañana
            if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, salida_m__lte = "12:59", salida_m__gte = "12:00") :
                q1.salida_m = hora
                q1.save()
        elif hora >= "18:00" and hora <= "22:00" :
            #salida tarde
            if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, salida_t__lte = "22:00", salida_t__gte = "18:00") :
                q1.salida_t = hora
                q1.save()
        else:
            if hora >= "08:16" and hora <= "11:59" :
                #entrada mañana tarde
                if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_m__lte = "11:59", entrada_m__gte = "08:16") :
                    q1.entrada_m = hora
                    q1.obs_m = 'RETRASO'
                    q1.save()
            if hora >= "14:16" and hora <= "17:59" :
                #Entrada tarde retraso
                if not Asistencia.objects.filter(empleado_id = emple.id, fecha = hoy, entrada_t__lte = "17:59", entrada_t__gte = "14:16") :
                    q1.entrada_t = hora
                    q1.obs_t = 'RETRASO'
                    q1.save()
            if hora >= "22:01" and hora <= "05:59" :
                return HttpResponseRedirect('/view/kardex/'+str(emple.id)+'/')
            else :
                return HttpResponseRedirect('/view/kardex/'+str(emple.id)+'/')
        return HttpResponseRedirect('/view/kardex/'+str(emple.id)+'/')
    else:
        return HttpResponseRedirect('/view/kardex/'+str(emple.id)+'/')



@permission_required('personal.add_observacion', login_url="/user/login")
def new_observacion(request, cod_emple):
    if request.method == 'POST' :
        formulario = ObservacionForm(request.POST, request.FILES)
        if formulario.is_valid():

            Observacion.objects.create(
                                        tipo = formulario.cleaned_data['tipo'],
                                        descripcion = formulario.cleaned_data['descripcion'],
                                        fecha = datetime.datetime.now(),
                                        empleado_id = cod_emple,
                                        )
            #formulario.save()
            return HttpResponseRedirect('/personal/option')
    else:
        formulario = ObservacionForm()
    return  render_to_response('personal/new_observacion.html', {'formulario' :formulario}, context_instance=RequestContext(request))



@permission_required('personal.add_permiso', login_url="/user/login")
def new_permiso(request, cod_emple):
    if request.method == 'POST' :
        formulario = PermisoForm(request.POST, request.FILES)
        if formulario.is_valid():
            Permiso.objects.create(
                                    descripcion = formulario.cleaned_data['descripcion'],
                                    fecha = datetime.datetime.now(),
                                    tiempo = formulario.cleaned_data['tiempo'],
                                    empleado_id = cod_emple,
                                   )
            return HttpResponseRedirect('/personal/option')
    else:
        formulario = PermisoForm()
    return  render_to_response('personal/new_observacion.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('personal.select_cargo_cambio', login_url="/user/login")
def select_personal(request):
    hoy = datetime.datetime.now()
    empleado=Empleados.objects.all()
    contratos = contratacion.objects.filter(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO')
    return render_to_response('personal/cambio_personal.html', {'empleados' :empleado, 'contratos':contratos}, context_instance=RequestContext(request))



@permission_required('personal.select_cargo_cambio', login_url="/user/login")
def cambio_cargo(request, empleado_cod):
    cargo = Cargos.objects.all()
    q1 = cargo.distinct().values('unidad_id')
    unidad = Unidades.objects.filter(id__in = q1)
    return render_to_response('personal/cargo_cambio.html', {
                                'cargos' :cargo, 
                                'unidades':unidad,
                                'empleado_cod' :empleado_cod,
                                }, context_instance=RequestContext(request))


@permission_required('personal.add_moviidad', login_url="/user/login")
def empleado_cambio(request, cargo_cod, empleado_cod):
    contrato = contratacion.objects.get(empleado_id = int(empleado_cod), estado = 'ACTIVO')
    moviidad.objects.create(
                            contrato_id = contrato.id,
                            cargo_id = int(cargo_cod),
                            fecha = datetime.datetime.now(),
                            )
    contrato.estado = 'INACTIVO'
    contrato.fecha_salida = datetime.datetime.now()
    contratacion.objects.create(
                                fecha_entrada = datetime.datetime.now(),
                                fecha_salida = contrato.fecha_salida,
                                estado = 'ACTIVO',
                                sueldo = contrato.sueldo,
                                descuento = contrato.descuento,
                                empleado_id = contrato.empleado_id,
                                cargo_id = int(cargo_cod),
                                )
    contrato.save()
    return HttpResponseRedirect('/personal')


def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privado')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            #users = User.objects.get(username = usuario)
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    #request.session['color']='red'
                    if 'next' in request.GET:
                        return HttpResponseRedirect(str(request.GET['next']))
                    else:
                        #request.user.message_set.create(
                        #    message="Inicio De Sesión Correcto"
                        #)
                        return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('user/noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('user/nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('user/user_login.html',{'formulario':formulario}, context_instance=RequestContext(request))



@login_required(login_url='/user/login')
def privado(request) :
    usuario = request.user
    return render_to_response('user/privado.html', {'usuario' :usuario}, context_instance=RequestContext(request))

@login_required(login_url='/user/login')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/user/login')
def reset_pass(request):
    if request.method == 'POST' :
        formulario = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/user/login')
    else:
        formulario = AdminPasswordChangeForm(user=request.user)
    return  render_to_response('user/reset_pass.html', {'formulario' :formulario}, context_instance=RequestContext(request))


@permission_required('personal.qr_empleados', login_url="/user/login")
def tarjeta_empleado(request, ci_emple):
    empleado = get_object_or_404(Empleados, ci = ci_emple)
    direccion = "http://192.168.43.124:90/asistencia/"+str(empleado.ci)+"/"
    return render_to_response('personal/qr.html', {'empleado' :empleado, 'direccion' :direccion}, context_instance=RequestContext(request))

@permission_required('personal.show_contrato', login_url="/user/login")
def view_contrato(request, cod_emple):
    q1 = get_object_or_404(Empleados, pk = cod_emple)
    hoy = datetime.datetime.now()
    q2 = contratacion.objects.get(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO', empleado_id = cod_emple)
    return HttpResponseRedirect("/contrato/show/"+str(q2.id)+"/0/")

@permission_required('personal.list_asistencia', login_url="/user/login")
def planilla_asistencia(request):
    hoy = datetime.datetime.now()
    q2 = contratacion.objects.filter(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO').values('empleado_id')
    empleado = Empleados.objects.filter(id__in = q2)
    asistencia = Asistencia.objects.filter(empleado_id__in=empleado)
    return render_to_response('personal/planilla_asistencia.html', {'empleados' :empleado,
                                                }, context_instance=RequestContext(request))

@permission_required('personal.fechas_asistencia', login_url="/user/login")
def seleccion_fechas(request, cod_emple):
    hoy = datetime.datetime.now()
    contrato = contratacion.objects.get(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO', empleado_id=cod_emple)
        #get_object_or_404(contratacion, pk = cod_emple)
    if request.method == 'POST' :
        formulario = FechasForm(request.POST)
        if formulario.is_valid():
            fecha_ini = request.POST['fecha_ini']
            fecha_fin = request.POST['fecha_fin']

            return HttpResponseRedirect("/planilla/detalle/"+cod_emple+"/"+fecha_ini+"/"+fecha_fin+"/0/")
    else:
        formulario = FechasForm()
    return  render_to_response('personal/seleccion_fechas.html', {'formulario' :formulario,
                                                                  'contrato':contrato,
                                                                }, context_instance=RequestContext(request))


@permission_required('personal.detalle_asistencia', login_url="/user/login")
def detalle_asistencia(request, id, dia_ini, mes_ini, anho_ini, dia_fin, mes_fin, anho_fin, pdf):
    hoy = datetime.datetime.now()
    fecha_ini =  date(int(anho_ini), int(mes_ini), int(dia_ini))
    fecha_fin = date(int(anho_fin), int(mes_fin), int(dia_fin))
    flag = True
    fechas = []
    d = fecha_ini
    while flag:
        fechas+=[d]
        d=d+timedelta(days=1)
        if d >= fecha_fin :
            flag = False

    empleado = get_object_or_404(Empleados, pk = id)
    contrato = contratacion.objects.get(fecha_salida__gte = hoy, fecha_entrada__lte=hoy, estado='ACTIVO', empleado_id=empleado.id)
    asistencia = Asistencia.objects.filter(empleado_id = empleado.id, fecha__gte = contrato.fecha_entrada)
    if not int(pdf):
        return render_to_response('personal/detalle_asistencia.html', {
                                                                    'mes' :fechas,
                                                                    'cod_emple':id,
                                                                    'fecha_ini':fecha_ini,
                                                                    'fecha_fin':fecha_fin,
                                                                    'empleado':empleado,
                                                                    'asistencia':asistencia,
                                                                }, context_instance=RequestContext(request))
    else:
        html = render_to_string('personal/detalle_asistencia_pdf.html', {'pagesize':'Letter',
                                                                    'mes' :fechas,
                                                                   'empleado':empleado,
                                                                   'asistencia':asistencia,
                                                                }, context_instance=RequestContext(request))
        return generar_pdf(html)


@permission_required('personal.change_asistencia', login_url="/user/login")
def asistencia_editar(request, id, dia_ini, mes_ini, anho_ini, dia_fin, mes_fin, anho_fin, asis_id):
    fecha_ini =  date(int(anho_ini), int(mes_ini), int(dia_ini))
    fecha_fin = date(int(anho_fin), int(mes_fin), int(dia_fin))
    asistencia = get_object_or_404(Asistencia, pk=asis_id)
    if request.method == 'POST' :
        formulario = AsistenciaFormEdid(request.POST, instance=asistencia)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/planilla/detalle/"+id+"/"+dia_ini+"/"+mes_ini+"/"+anho_ini+"/"+dia_fin+"/"+mes_fin+"/"+anho_fin+"/0/")
    else:
        formulario = AsistenciaFormEdid(instance = asistencia)
    return  render_to_response('personal/editar_asistencia.html', {'formulario' :formulario,
                                                                   'id':id,
                                                                   'fecha_ini':fecha_ini,
                                                                   'fecha_fin':fecha_fin,
                                                                }, context_instance=RequestContext(request))



def generar_pdf(html, numero = 1):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    links = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-16")), result, link_callback=links)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def get_full_path_x(request):
    full_path = ('http', ('', 's')[request.is_secure()], '://',
    request.META['HTTP_HOST'], request.path)
    return ''.join(full_path)


@permission_required('personal.list_kardex_empleado', login_url="/user/login")
def view_empleado_kardex(request):
    empleados = Empleados.objects.all()
    return render_to_response('personal/view_empleado_kardex.html', {'empleados':empleados,
                                                                }, context_instance=RequestContext(request))



def kardex_empleado(request, cod_emple):
    q1 = get_object_or_404(Empleados, pk=cod_emple)
    q2 = contratacion.objects.filter(empleado_id = cod_emple)
    q5 = moviidad.objects.filter(contrato_id__in = q2)
    q3 = Cargos.objects.filter()

    q4 = Observacion.objects.filter(empleado_id = cod_emple)

    return render_to_response('personal/kardex_personal.html', {
                                'empleado':q1,
                                'contratos':q2,
                                'movilidad':q5,
                                'observaciones':q4,
                            }, context_instance=RequestContext(request))


@permission_required('personal.list_contrato_empleado', login_url="/user/login")
def seleccion_empleado_contrato(request):
    hoy = datetime.datetime.now()
    q1 = contratacion.objects.filter(fecha_entrada__lte=hoy, fecha_salida__gte=hoy, estado='ACTIVO')
    q2 = q1.values('empleado_id')
    q3 = Empleados.objects.filter(id__in = q2)
    return render_to_response('personal/contratos_terminar.html',{'contratos':q1,'empleados':q3}, context_instance=RequestContext(request))

@permission_required('personal.delete_contratacion', login_url="/user/login")
def terminar_contrato(requesr, id_contrato):
    q1 = get_object_or_404(contratacion, pk=id_contrato)
    q1.estado = 'INACTIVO'
    q1.fecha_salida = datetime.datetime.now()
    q1.save()
    return HttpResponseRedirect('/contrato/seleccionar/')
