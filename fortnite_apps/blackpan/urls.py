from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.blackpan, name='black_pan'),
    url(r'^participantes', views.blackpan_participantes, name='black_pan_participantes' ),
    url(r'^resultados', views.blackpan_resultados, name='black_pan_resultados' ),
    url(r'^premios', views.blackpan_premios, name='black_pan_premios' ),
    url(r'^tabla', views.blackpan_tabla, name='black_pan_tabla' ),
    url(r'^terminos', views.blackpan_terminos, name='black_pan_terminos' )
]
