from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from sistema.models import Perfil
import requests
from decimal import Decimal
from django.core.mail import send_mail
import time
from .utils import comenzar_torneo_rq, finalizar_torneo_rq, mail_comienzo_torneo_rq, calcular_puntajes_general_rq
from rq import Queue
from worker import conn
import django_rq
q = Queue(connection=conn)

class PerfilInline (admin.StackedInline):
    model = Perfil
    can_delete = False

def mail_comienzo_torneo(modeladmin, request, queryset):
    django_rq.enqueue(mail_comienzo_torneo_rq)
mail_comienzo_torneo.short_description = "MAIL POR COMENZAR"

def resetear_todo(modeladmin, request, queryset):
    Perfil.objects.update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', general='0', prepartidas_1='0', postpartidas_1='0', muertes_1='0', kd='0')
    Perfil.objects.update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0', muertes_2='0')
    Perfil.objects.update(kills_totales='0', wins_totales='0', kills_liga='0', muertes_liga='0', muertes_totales='0', pretop5_1='0', posttop5_1='0', top5_1='0')
resetear_todo.short_description = "XXX Resetear TODO XXX"

def resetear_torneo(modeladmin, request, queryset):
    Perfil.objects.update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', prepartidas_1='0', postpartidas_1='0', partidas_1='0')
    Perfil.objects.update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0', partidas_2='0')
resetear_torneo.short_description = "XXX Resetear torneo XXX"

def comenzar_torneo(modeladmin, request, queryset):
    django_rq.enqueue(comenzar_torneo_rq)
comenzar_torneo.short_description = "COMENZAR TORNEO"

def finalizar_torneo(modeladmin, request, queryset):
    django_rq.enqueue(finalizar_torneo_rq)
finalizar_torneo.short_description = "FINALIZAR TORNEO"

def calcular_puntajes_general(modeladmin, request, queryset):
    django_rq.enqueue(calcular_puntajes_general_rq)
calcular_puntajes_general.short_description = "--CALCULAR GENERALES--"

class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]
    list_display = ( 'equipo', 'usuario1', 'usuario2', 'plataforma', 'email', 'comentario', 'ver', 'prekills', 'postkills')

    def ver(self, obj):
        return obj.perfil.VERIFICACION_2
    def equipo(self, obj):
        return obj.perfil.equipo
    def prekills(self, obj):
        return obj.perfil.prekills_1
    def postkills(self, obj):
        return obj.perfil.postkills_1
    def usuario2(self, obj):
        return obj.first_name
    def usuario1(self, obj):
        return obj.username
    def plataforma(self, obj):
        return obj.last_name
    def comentario(self, obj):
        return obj.perfil.comentario

    #get_author.short_description = 'Author'
    #get_author.admin_order_field = 'book__author'

    ordering = ('-date_joined', )
    list_filter = ('perfil__VERIFICACION_2', 'last_name')
    actions = [resetear_torneo, resetear_todo, mail_comienzo_torneo, comenzar_torneo, finalizar_torneo, calcular_puntajes_general]

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipo', 'VERIFICACION_2')
    ordering = ('VERIFICACION_2', )
    actions = [resetear_torneo, resetear_todo, mail_comienzo_torneo, comenzar_torneo, finalizar_torneo]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Perfil, PerfilAdmin)



# Register your models here.
