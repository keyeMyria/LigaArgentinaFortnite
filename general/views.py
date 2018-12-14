from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import (
    Http404,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.http import HttpResponse
from allauth.account.decorators import verified_email_required
from fortnite_apps.sistema.models import Perfil
from django.contrib.auth.models import User


def pagina_principal(request):
    #return HttpResponse('homepage')
    return render(request, 'general/pagina_principal.html')

def contacto(request):
    #return HttpResponse('homepage')
    return render(request, 'general/contacto.html')

# Create your views here.
