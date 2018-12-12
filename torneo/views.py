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
from fortnite_apps.sistema.models import Perfil
from django.contrib.auth.models import User


#TEST
def test(request):
    #return HttpResponse('homepage')
    return render(request, 'test.html')

def contacto(request):
    #return HttpResponse('homepage')
    return render(request, 'contacto.html')

def homepage(request):
    #return HttpResponse('homepage')
    return render(request, 'homepage.html')

def reglas(request):
    #return HttpResponse('homepage')
    return render(request, 'reglas.html')

def premios(request):
    #return HttpResponse('homepage')
    return render(request, 'premios.html')
