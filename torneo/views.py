from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    #return HttpResponse('homepage')
    return render(request, 'homepage.html')

def reglas(request):
    #return HttpResponse('homepage')
    return render(request, 'reglas.html')

def premios(request):
    #return HttpResponse('homepage')
    return render(request, 'premios.html')
