from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resultados/pc', views.resultadospc, name='resultados_pc'),
    url(r'^resultados/ps4', views.resultadosps4, name='resultados_ps4'),
    url(r'^resultados/general_pc', views.general_pc, name='general_pc'),
    url(r'^resultados/general_ps4', views.general_ps4, name='general_ps4'),
    url(r'^resultados/no', views.resultados_no, name='resultados_no_publicados'),
]
