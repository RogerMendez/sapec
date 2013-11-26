from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.MEDIA_ROOT,} ),
    
    # ABIERTO
    url(r'^$', 'abierto.views.index'),
    #ADMINISTRADOR
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #ORGANIZACION
    #unidad
    url(r'^organizacion/$', 'organizacion.views.index_organizacion'),
    url(r'^unidad/new/$', 'organizacion.views.nueva_unidad'),
    url(r'^unidad/option/$', 'organizacion.views.option_unidad'),
    url(r'^unidad/update/(?P<id_unidad>\d+)/$', 'organizacion.views.update_unidad'),
    #url(r'^show/$', 'ejemplo.views.show_persona'),
    url(r'^unidad/planificacion/(?P<id_cargo>\d+)/$', 'organizacion.views.cargo_plani'),
    #planificacion
    url(r'^planificacion/new/$', 'organizacion.views.nueva_plani'),
    url(r'^planificacion/option/$', 'organizacion.views.option_plani'),
    url(r'^planificacion/update/(?P<id_plani>\d+)/$', 'organizacion.views.update_planificacion'),
    url(r'^planificacion/cancel/(?P<id_plani>\d+)/$', 'organizacion.views.cancel_plani'),

    url(r'^planificacion/seleccion/$', 'organizacion.views.view_planificaciones_cargo'),

    url(r'^planificacion/cargo/(?P<id_cargo>\d+)/$', 'organizacion.views.planificacion_cargo'),

    #CARGOS

    url(r'^cargo/new/$', 'organizacion.views.new_cargo'),
    url(r'^cargo/option/$', 'organizacion.views.option_cargo'),
    url(r'^cargo/update/(?P<id_cargo>\d+)/$', 'organizacion.views.update_cargo'),
    #funcion
    url(r'^funcion/new/$', 'organizacion.views.new_funcion'),
    url(r'^funcion/option/$', 'organizacion.views.option_function'),
    url(r'^funcion/update/(?P<id_funcion>\d+)/$', 'organizacion.views.update_funcion'),
    url(r'^funcion/delete/(?P<id_funcion>\d+)/$', 'organizacion.views.delete_funcion'),
    #CONOCIMIENTO
    url(r'^conocimiento/new/$', 'organizacion.views.new_conocimiento'),
    url(r'^conocimiento/option/$', 'organizacion.views.option_conocimiento'),
    url(r'^conocimiento/update/(?P<cono_id>\d+)/$', 'organizacion.views.update_conocimiento'),
    url(r'^conocimiento/delete/(?P<cono_id>\d+)/$', 'organizacion.views.delete_conocimiento'),

    url(r'^seleccion/cargo/$', 'organizacion.views.seleccion_cargos_cono'),
    url(r'^conocimiento/funcion/(?P<cargo_id>\d+)/$', 'organizacion.views.conocimiento_funciones'),

    #PERSONAL
    url(r'^personal/$', 'personal.views.home'),
    url(r'^personal/option/$', 'personal.views.option_empleado'),
    url(r'^personal/update/(?P<empleado_id>\d+)/$', 'personal.views.update_empleado'),
    url(r'^personal/option/update/$', 'personal.views.option_update_empleado'),
    url(r'^personal/contrato/empleado/$', 'personal.views.view_contratacion'),
    url(r'^personal/observacion/empleado/$', 'personal.views.registro_observacion_observacion'),

    url(r'^personal/kardex/', 'personal.views.view_empleado_kardex'),
    url(r'^view/kardex/(?P<cod_emple>\d+)/$', 'personal.views.kardex_empleado'),

    url(r'^profesion/new/$', 'personal.views.new_profesion'),

    url(r'^planilla/asistencia/$', 'personal.views.planilla_asistencia'),
    url(r'^planilla/detalle/(?P<id>\d+)/(?P<dia_ini>\d+)/(?P<mes_ini>\d+)/(?P<anho_ini>\d+)/(?P<dia_fin>\d+)/(?P<mes_fin>\d+)/(?P<anho_fin>\d+)/(?P<pdf>\d+)/$', 'personal.views.detalle_asistencia'),

    url(r'^asistencia/editar/(?P<id>\d+)/(?P<dia_ini>\d+)/(?P<mes_ini>\d+)/(?P<anho_ini>\d+)/(?P<dia_fin>\d+)/(?P<mes_fin>\d+)/(?P<anho_fin>\d+)/(?P<asis_id>\d+)/$', 'personal.views.asistencia_editar'),

    url(r'^planilla/salario/$', 'remuneraciones.views.planilla_sueldos'),
    url(r'^planilla/detalle/sueldo/(?P<id_emple>\d+)/$', 'remuneraciones.views.detalle_planilla'),

    url(r'^planilla/seleccion/(?P<cod_emple>\d+)/$', 'personal.views.seleccion_fechas'),

    #CONTRATO
    url(r'^contrato/cargo/$', 'personal.views.cargos_contrato'),
    url(r'^contrato/personal/(?P<cod_cargo>\d+)/$', 'personal.views.new_empleado'),
    url(r'^contrato/new/(?P<empleado_ci>\d+)/(?P<cargo_id>\d+)/$', 'personal.views.new_contrato'),
    url(r'^contrato/show/(?P<cod_contrato>\d+)/(?P<pdf>\d+)/$', 'personal.views.show_contrato'),
    url(r'^qr/show/(?P<ci_emple>\d+)/$', 'personal.views.tarjeta_empleado'),
    url(r'^show/contrato/(?P<cod_emple>\d+)/$', 'personal.views.view_contrato'),

    url(r'^contrato/seleccionar/$', 'personal.views.seleccion_empleado_contrato'),
    url(r'^contrato/terminar/(?P<id_contrato>\d+)/$', 'personal.views.terminar_contrato'),

    url(r'^usuario/contrataciones/$', 'personal.views.contrato_usuario' ),

    #ASISTENNCIA
    url(r'^personal/asistencia/$', 'personal.views.new_asistencia'),
    url(r'^asistencia/(?P<ci_emple>\d+)/$', 'personal.views.asistecia'),
    #OBSERVACION
    url(r'^observacion/new/(?P<cod_emple>\d+)/$', 'personal.views.new_observacion'),
    #PERMISO
    url(r'^permiso/new/(?P<cod_emple>\d+)/$', 'personal.views.new_permiso'),
    #MOVILIDAD
    url(r'^empleado/cambio/$', 'personal.views.select_personal'),
    url(r'^cargo/cambio/(?P<empleado_cod>\d+)/$', 'personal.views.cambio_cargo'),
    url(r'^empleado/cambio/(?P<cargo_cod>\d+)/(?P<empleado_cod>\d+)/$', 'personal.views.empleado_cambio'),
    url(r'^empleado/razon/cambio/(?P<cod_cambio>\d+)', 'personal.views.razon_cambio'),
    #REMUNERACION
    url(r'^remuneracion/$', 'remuneraciones.views.home'),
    #PAGOS
    url(r'^pago/empleado/$', 'remuneraciones.views.pago_empleado'),

    #DESCUENTOS
    url(r'^descuento/empleado/$', 'remuneraciones.views.descuento_empleado'),
    #FORDES
    url(r'^pago/new/(?P<cod_emple>\d+)/$', 'remuneraciones.views.new_pago'),
    url(r'^descuento/new/(?P<cod_emple>\d+)/$', 'remuneraciones.views.new_descuento'),

    #USUARIOS
    url(r'^user/login/$', 'personal.views.ingresar'),
    url(r'^privado/$', 'personal.views.privado'),
    url(r'^salir/$', 'personal.views.cerrar'),
    url(r'^reset/password/$', 'personal.views.reset_pass'),


    url(r'^report/unidad/pdf/(?P<pdf>\d+)/$', 'organizacion.views.unidad_pdf'),
    url(r'^report/cargo/pdf/(?P<pdf>\d+)/$', 'organizacion.views.cargos_pdf'),
    url(r'^report/cargo/noempleado/(?P<pdf>\d+)/$', 'organizacion.views.cargos_no_empleado'),


    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += staticfiles_urlpatterns()