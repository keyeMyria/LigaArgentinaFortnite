from django.shortcuts import render, redirect
from django.http import (
    Http404,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from allauth.account.decorators import verified_email_required
from . import forms
from .models import Perfil
from django.contrib.auth.models import User



def resultadospc(request):
    userobjectpc = Perfil.objects.filter(user__last_name='pc', VERIFICACION_2=True).order_by('-puntos')
    return render(request, 'sistema/resultados_pc.html', {'participantes': userobjectpc})

def resultadosps4(request):
    userobjectpc = Perfil.objects.filter(user__last_name='psn', VERIFICACION_2=True).order_by('-puntos')
    return render(request, 'sistema/resultados_ps4.html', {'participantes': userobjectpc})

def resultados_no(request):
    return render(request, 'sistema/resultados_no_publicados.html')

def general_pc(request):
    userobjectpc = Perfil.objects.filter(user__last_name='pc', VERIFICACION_2=True).order_by('-general', '-kd')
    return render(request, 'sistema/general_pc.html', {'participantes': userobjectpc})

def general_ps4(request):
    userobjectpc = Perfil.objects.filter(user__last_name='psn', VERIFICACION_2=True).order_by('-general', '-kd')
    return render(request, 'sistema/general_ps4.html', {'participantes': userobjectpc})
# Create your views here.
