from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
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

)
