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

    #UNIDADES
    url(r'^unidad/$', 'organizacion.views.index_unidad'),
    url(r'^unidad/new/$','organizacion.views.new_unidad'),
    url(r'^unidad/option/update/$', 'organizacion.views.option_update'),
    url(r'^unidad/update/(?P<id_unidad>\d+)/$', 'organizacion.views.update_unidad'),
    url(r'^unidad/option/detalle/$', 'organizacion.views.option_detalle'),
    url(r'^unidad/detail/(?P<id_unidad>\d+)/$', 'organizacion.views.detail_unidad'),
    url(r'^unidad/reporte/unidades/(?P<pdf>\d+)/$', 'organizacion.views.unidades_pdf'),
    url(r'^unidad/reporte/unidades/sin/cargo/(?P<pdf>\d+)/$', 'organizacion.views.unidades_sin_cargo'),

    #CARGOS
    url(r'^cargo/$', 'organizacion.views.index_cargo'),
    url(r'^cargo/new/$','organizacion.views.new_cargo'),
    url(r'^cargo/option/update/$', 'organizacion.views.option_update_cargo'),
    url(r'^cargo/update/(?P<id_cargo>\d+)/$', 'organizacion.views.update_cargo'),
    url(r'^cargo/option/detalle/$', 'organizacion.views.option_detalle_cargo'),
    url(r'^cargo/detail/(?P<id_cargo>\d+)/$', 'organizacion.views.detalle_cargo'),
    url(r'^cargo/reporte/cargos/(?P<pdf>\d+)/$', 'organizacion.views.cargos_pdf'),

    #PLANIFICACIONES
    url(r'^planificacion/$', 'organizacion.views.index_planificacion'),
    url(r'^planificacion/new/$', 'organizacion.views.new_planificacion'),

)
