from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

admin.autodiscover()

urlpatterns = patterns('',

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
    #CARGOS
    url(r'^cargo/$', 'organizacion.views.index_cargo'),
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
    #PERSONAL
    url(r'^personal/$', 'personal.views.home'),
    url(r'^personal/option/$', 'personal.views.option_empleado'),
    url(r'^personal/update/(?P<empleado_id>\d+)/$', 'personal.views.update_empleado'),

    url(r'^profesion/new$', 'personal.views.new_profesion'),

    #CONTRATO
    url(r'^contrato/cargo/$', 'personal.views.cargos_contrato'),
    url(r'^contrato/personal/(?P<cod_cargo>\d+)/$', 'personal.views.new_empleado'),
    url(r'^contrato/new/(?P<empleado_ci>\d+)/(?P<cargo_id>\d+)/$', 'personal.views.new_contrato'),
    url(r'^contrato/show/(?P<cod_contrato>\d+)/(?P<pdf>\d+)/$', 'personal.views.show_contrato'),
    url(r'^qr/show/(?P<ci_emple>\d+)/$', 'personal.views.tarjeta_empleado'),
    url(r'^show/contrato/(?P<cod_emple>\d+)/$', 'personal.views.view_contrato'),
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
    #REMUNERACION
    url(r'^remuneracion/$', 'remuneraciones.views.home'),
    #PAGOS
    url(r'^pago/empleado/$', 'remuneraciones.views.pago_empleado'),
    url(r'^pago/new/(?P<cod_emple>\d+)/$', 'remuneraciones.views.new_pago'),
    url(r'^descuento/new/(?P<cod_emple>\d+)/$', 'remuneraciones.views.new_descuento'),

    #USUARIOS
    url(r'^user/login/$', 'personal.views.ingresar'),
    url(r'^privado/$', 'personal.views.privado'),
    url(r'^salir/$', 'personal.views.cerrar'),


    url(r'^report/unidad/pdf/(?P<pdf>\d+)/$', 'organizacion.views.unidad_pdf'),
    url(r'^report/cargo/pdf/(?P<pdf>\d+)/$', 'organizacion.views.cargos_pdf'),
    url(r'^report/cargo/noempleado/(?P<pdf>\d+)/$', 'organizacion.views.cargos_no_empleado'),


    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += staticfiles_urlpatterns()