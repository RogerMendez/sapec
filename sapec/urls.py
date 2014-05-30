from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.MEDIA_ROOT,} ),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'users.views.home'),

    #USUARIOS
    url(r'^login/$', 'users.views.loguet_in'),
    url(r'^perfil/$', 'users.views.private'),
    url(r'^user/resetpass/$', 'users.views.reset_pass'),
    url(r'^logout/$', 'users.views.loguet_out'),
    url(r'^user/new/$', 'users.views.new_user'),
    url(r'^user/confirmar/$', 'users.views.confirmation_user'),

    #UNIDADES
    url(r'^unidad/$', 'organizacion.views.index_unidad'),
    url(r'^unidad/new/$','organizacion.views.new_unidad'),
    url(r'^unidad/option/update/$', 'organizacion.views.option_update'),
    url(r'^unidad/update/(?P<id_unidad>\d+)/$', 'organizacion.views.update_unidad'),
    url(r'^unidad/option/detail/$', 'organizacion.views.option_detalle'),
    url(r'^unidad/detail/(?P<id_unidad>\d+)/$', 'organizacion.views.detail_unidad'),
    url(r'^unidad/reporte/unidades/(?P<pdf>\d+)/$', 'organizacion.views.unidades_pdf'),
    url(r'^unidad/reporte/unidades/sin/cargo/(?P<pdf>\d+)/$', 'organizacion.views.unidades_sin_cargo'),

    #CARGOS
    url(r'^cargo/$', 'organizacion.views.index_cargo'),
    url(r'^cargo/new/$','organizacion.views.new_cargo'),
    url(r'^cargo/option/update/$', 'organizacion.views.option_update_cargo'),
    url(r'^cargo/update/(?P<id_cargo>\d+)/$', 'organizacion.views.update_cargo'),
    url(r'^cargo/option/detail/$', 'organizacion.views.option_detalle_cargo'),
    url(r'^cargo/detail/(?P<id_cargo>\d+)/$', 'organizacion.views.detalle_cargo'),
    url(r'^cargo/reporte/cargos/(?P<pdf>\d+)/$', 'organizacion.views.cargos_pdf'),

    #PLANIFICACIONES
    url(r'^planificacion/$', 'organizacion.views.index_planificacion'),
    url(r'^planificacion/new/$', 'organizacion.views.new_planificacion'),
    url(r'^planificacion/option/update/$', 'organizacion.views.option_update_planificacion'),
    url(r'^planificacion/update/(?P<id_plani>\d+)/$', 'organizacion.views.update_planificacion'),
    url(r'^planificacion/option/detail/$', 'organizacion.views.option_detalle_planificacion'),
    url(r'^planificacion/detail/(?P<id_plani>\d+)/$', 'organizacion.views.detalle_planificacion'),
    url(r'^planificacion/option/cancel/$', 'organizacion.views.option_cancel_planificacion'),
    url(r'^planificacion/cancel/(?P<id_plani>\d+)/$', 'organizacion.views.cancel_planificacion'),
    url(r'^planificacion/cargo/$', 'organizacion.views.planificaciones_cargos'),
    url(r'^planificacion/cargo/(?P<id_cargo>\d+)/$', 'organizacion.views.planificaciones_cargo'),

    #PERSONAL
    url(r'^personal/$', 'personal.views.index_personal'),
    url(r'^personal/pdf/(?P<persona_id>\d+)/$', 'personal.views.kardex_personal_pdf'),
    url(r'^personal/update/$', 'personal.views.completar_datos_persona'),
    url(r'^personal/show/$', 'personal.views.show_datos_persona'),
    url(r'^personal/estudio/show/$', 'personal.views.show_estudios'),
    url(r'^personal/estudio/new/$', 'personal.views.new_estudio'),
    url(r'^personal/estudio/update/(?P<id_estudio>\d+)/$', 'personal.views.update_estudio'),
    url(r'^personal/estudio/delete/(?P<id_estudio>\d+)/$', 'personal.views.delete_estudio'),
    url(r'^personal/oestudio/show/$', 'personal.views.show_otros_estudios'),
    url(r'^personal/oestudio/new/$', 'personal.views.new_otro_estudio'),
    url(r'^personal/oestudio/update/(?P<id_oestudio>\d+)/$', 'personal.views.update_otro_estudio'),
    url(r'^personal/oestudio/delete/(?P<id_oestudio>\d+)/$', 'personal.views.delete_otro_estudio'),
    url(r'^personal/experiencia/show/$', 'personal.views.show_experiencias_trabajo'),
    url(r'^personal/experiencia/new/$', 'personal.views.new_experiencia'),
    url(r'^personal/experiencia/update/(?P<id_experiencia>\d+)/$', 'personal.views.update_experiencia_trabajo'),
    url(r'^personal/experiencia/delete/(?P<id_experiencia>\d+)/$', 'personal.views.delete_experiencia_trabajo'),
    url(r'^personal/idiomas/show/$', 'personal.views.show_idiomas'),
    url(r'^personal/idiomas/new/$', 'personal.views.new_idioma'),
    url(r'^personal/idiomas/update/(?P<id_idioma>\d+)/$', 'personal.views.update_idioma'),
    url(r'^personal/idiomas/delete/(?P<id_idioma>\d+)/$', 'personal.views.delete_idioma'),
    url(r'^personal/qr/list/$', 'personal.views.select_personal_qr'),
    url(r'^personal/qr/show/(?P<id_persona>\d+)/$', 'personal.views.tarjeta_qr'),
    url(r'^personal/qr/$', 'personal.views.my_tarjeta_qr'),
    url(r'^personal/kardex/select/$', 'personal.views.select_personal_kardex'),
    url(r'^personal/kardex/view/(?P<id_persona>\d+)/$', 'personal.views.view_kardex'),
    url(r'^personal/kardex/empresa/select/$', 'personal.views.select_personal_kardex_empresa'),
    url(r'^personal/kardex/empresa/view/(?P<id_persona>\d+)/$', 'personal.views.view_kardex_persona_empresa'),

    #CONTRATACION
    url(r'^contratacion/show/$', 'contratacion.views.show_contrataciones'),
    url(r'^contratacion/cargo/select/$', 'contratacion.views.select_cargo'),
    url(r'^contratacion/persona/select/(?P<id_cargo>\d+)/$', 'contratacion.views.select_persona'),
    url(r'^contratacion/new/persona/(?P<id_cargo>\d+)/$', 'contratacion.views.new_persona'),
    url(r'^contratacion/persona/new/(?P<id_cargo>\d+)/(?P<id_persona>\d+)/$', 'contratacion.views.new_contrato'),
    url(r'^contratacion/about/$', 'contratacion.views.list_contratos_informacion'),
    url(r'^contratacion/view/(?P<id_persona>\d+)/$', 'contratacion.views.view_contrato'),
    url(r'^contratacion/movilidad/show/$', 'contratacion.views.list_contratos_movilidad'),
    url(r'^contratacion/movilidad/cargo/select/(?P<id_contrato>\d+)/$', 'contratacion.views.select_cargo_cambio'),
    url(r'^contratacion/movilidad/new/razon/(?P<id_cargo>\d+)/(?P<id_contrato>\d+)/$', 'contratacion.views.new_cambio'),
    url(r'^contratacion/terminar/show/$', 'contratacion.views.list_contratos_terminar'),
    url(r'^contratacion/terminar/new/(?P<id_contrato>\d+)/$', 'contratacion.views.terminar_contrato'),

    #ASISTENCIA
    url(r'^asistencia/$', 'asistencia.views.index_asistencia'),
    url(r'^asistencia/new/$', 'asistencia.views.new_asistencia'),
    url(r'^asistencia/update/(?P<id_asistencia>\d+)/$', 'asistencia.views.update_asistencia'),
    url(r'^asistencia/detail/empleado/show/$', 'asistencia.views.personal_asistencia'),
    url(r'^asistencia/detail/fechas/seleccion/(?P<id_persona>\d+)/$', 'asistencia.views.seleccion_fechas_detalle'),
    url(r'^asistencia/detail/(?P<id_persona>\d+)/(?P<dia_ini>\d+)/(?P<mes_ini>\d+)/(?P<anho_ini>\d+)/(?P<dia_fin>\d+)/(?P<mes_fin>\d+)/(?P<anho_fin>\d+)/(?P<pdf>\d+)/$', 'asistencia.views.detalle_asistencia'),
    url(r'^asistencia/detail/empleado/show/fecha/$', 'asistencia.views.personal_asistencia_fecha'),
    url(r'^asistencia/historial/select/empleado/$', 'asistencia.views.select_persona_historial_mes'),
    url(r'^asistencia/historial/select/mes/(?P<id_persona>\d+)/$', 'asistencia.views.select_meses'),
    url(r'^asistencia/historial/view/mes/(?P<id_persona>\d+)/(?P<mes>\d+)/(?P<anho>\d+)/$', 'asistencia.views.view_historial_meses'),
    url(r'^asistencia/historial/anual/select/empleado/$', 'asistencia.views.select_persona_historial_anual'),
    url(r'^asistencia/historial/anual/select/year/(?P<id_persona>\d+)/$', 'asistencia.views.select_anho'),
    url(r'^asistencia/historial/anual/view/year/(?P<id_persona>\d+)/(?P<anho>\d+)/$', 'asistencia.views.view_historial_anual'),
    url(r'^asistencia/qr/$', 'asistencia.views.asistencia_qr'),

    #PERMISO
    url(r'^permiso/$', 'asistencia.views.index_permiso'),
    url(r'^permiso/persona/show/$', 'asistencia.views.select_persona_permiso'),
    url(r'^permiso/persona/new/(?P<id_persona>\d+)/$', 'asistencia.views.new_permiso'),

    #OBSERVACIONES
    url(r'^observacion/$', 'personal.views.index_observaciones'),
    url(r'^observacion/persona/show/$', 'personal.views.select_persona_observacion'),
    url(r'^observacion/persona/new/(?P<id_persona>\d+)/$', 'personal.views.new_observacion'),
    url(r'^observacion/list/$', 'personal.views.list_observaciones'),

    #REMUNERACIONES
    url(r'^remuneracion/$', 'remuneraciones.views.index_remuneracion'),
    url(r'^remuneracion/pagos/$', 'remuneraciones.views.otros_pagos'),
    url(r'^remuneracion/pagos/personas/show/$', 'remuneraciones.views.select_persona_pagos'),
    url(r'^remuneracion/pagos/new/(?P<id_contrato>\d+)/$', 'remuneraciones.views.new_pago'),
    url(r'^remuneracion/descuentos/$', 'remuneraciones.views.descuentos_index'),
    url(r'^remuneracion/descuentos/personas/show/$', 'remuneraciones.views.select_persona_descuentos'),
    url(r'^remuneracion/descuentos/new/(?P<id_contrato>\d+)/$', 'remuneraciones.views.new_descuento'),
    url(r'^planilla/sueldos/$', 'remuneraciones.views.planilla_sueldos'),


    #Otros
    url(r'^marcar/$', 'asistencia.views.insert_asistencia'),

)
