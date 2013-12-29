#encoding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth.forms import AdminPasswordChangeForm, AuthenticationForm, authenticate
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required

def home(request):
    return render_to_response('base.html', context_instance=RequestContext(request))

def loguet_in(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse(private))
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    if 'next' in request.GET:
                        return HttpResponseRedirect(str(request.GET['next']))
                    else:
                        return HttpResponseRedirect(reverse(private))
                else:
                    return render_to_response('user/noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('user/nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('user/user_login.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def loguet_out(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def private(request) :
    usuario = request.user
    return render_to_response('user/privado.html', {'usuario' :usuario}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def reset_pass(request):
    if request.method == 'POST' :
        formulario = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse(loguet_in))
    else:
        formulario = AdminPasswordChangeForm(user=request.user)
    return  render_to_response('user/reset_pass.html', {'formulario' :formulario}, context_instance=RequestContext(request))
