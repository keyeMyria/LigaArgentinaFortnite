from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    url(r'^contacto', views.contacto, name='contacto')
]
