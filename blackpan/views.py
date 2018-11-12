from django.http import HttpResponse
from django.shortcuts import render
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
from sistema.models import Perfil
from django.contrib.auth.models import User


def blackpan(request):
    #return HttpResponse('homepage')
    return render(request, 'black_pan/principal.html')

def blackpan_participantes(request):
    userobjectpc = Perfil.objects.filter(user__last_name='psn', VERIFICACION_2=True, black_pan='SI').order_by('-puntos')
    return render(request, 'black_pan/participantes.html', {'participantes': userobjectpc})

def blackpan_resultados(request):
    userobjectpc = Perfil.objects.filter(user__last_name='psn', VERIFICACION_2=True, black_pan='SI').order_by('-puntos')
    return render(request, 'black_pan/resultados.html', {'participantes': userobjectpc})

def blackpan_premios(request):
    #return HttpResponse('homepage')
    return render(request, 'black_pan/premios.html')

def blackpan_terminos(request):
    #return HttpResponse('homepage')
    return render(request, 'black_pan/terminos.html')
