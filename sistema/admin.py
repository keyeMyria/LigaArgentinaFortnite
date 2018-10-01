from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from sistema.models import Perfil
import requests
from decimal import Decimal
from django.core.mail import send_mail
import time


class PerfilInline (admin.StackedInline):
    model = Perfil
    can_delete = False

def mail_comienzo_torneo(modeladmin, request, queryset):
    for user in User.objects.all():
        send_mail('El torneo esta por comenzar!', 'Conectate y preparate!', 'mmquiroga10@gmail.com', [user.email])
mail_comienzo_torneo.short_description = "MAIL POR COMENZAR"

def resetear_todo(modeladmin, request, queryset):
    Perfil.objects.update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', general='0', prepartidas_1='0', postpartidas_1='0', partidas_1='0', kd='0')
    Perfil.objects.update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0', partidas_2='0')
    Perfil.objects.update(kills_totales='0', wins_totales='0', kills_liga='0', partidas_liga='0')
resetear_todo.short_description = "XXX Resetear TODO XXX"

def resetear_torneo(modeladmin, request, queryset):
    Perfil.objects.update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', prepartidas_1='0', postpartidas_1='0', partidas_1='0')
    Perfil.objects.update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0', partidas_2='0')
resetear_torneo.short_description = "XXX Resetear torneo XXX"

def comenzar_torneo(modeladmin, request, queryset):
    #ENVIAR MAIL DE COMIENZO
    #for user in User.objects.all():
    #    send_mail('EL TORNEO ACABA DE COMENZAR!', 'Conectate y comienza a jugar ya!', 'mmquiroga10@gmail.com', [user.email])

    #VARIABLES API
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.verificados.all()
    for user in usuarios:
        plataforma = user.user.last_name
        u1 = user.user.username
        u2 = user.user.first_name
        u1 = u1.replace(" ", "%20")
        u2 = u2.replace(" ", "%20")
        url1 = URL + plataforma + '/' + u1
        url2 = URL + plataforma + '/' + u2
        respuesta_1 = requests.get(url1, headers=headers)
        resultado_1 = respuesta_1.json()
        respuesta_2 = requests.get(url2, headers=headers)
        resultado_2 = respuesta_2.json()
        if 'error' in resultado_1.keys():
            no = no
        else:
            resultado_1 = respuesta_1.json()['lifeTimeStats']
            for r in resultado_1:
                if r['key'] == 'Wins':
                    prewins_1 = r['value']
                if r['key'] == 'Kills':
                    prekills_1 = r['value']
                if r['key'] == 'Matches Played':
                    prepartidas_1 = r['value']
            if 'error' in resultado_2.keys():
                no2 = no2
            else:
                resultado_2 = respuesta_2.json()['lifeTimeStats']
                for r in resultado_2:
                    if r['key'] == 'Wins':
                        prewins_2 = r['value']
                    if r['key'] == 'Kills':
                        prekills_2 = r['value']
                    if r['key'] == 'Matches Played':
                        prepartidas_2 = r['value']
                Perfil.objects.filter(user__username=u1).update(prekills_1=prekills_1, prewins_1=prewins_1, prepartidas_1=prepartidas_1, prekills_2=prekills_2, prewins_2=prewins_2, prepartidas_2=prepartidas_2)
comenzar_torneo.short_description = "COMENZAR TORNEO"

def finalizar_torneo_sin_calculos(modeladmin, request, queryset):
    #ENVIAR MAIL DE COMIENZO
    #for user in User.objects.all():
    #    send_mail('EL TORNEO ACABA DE COMENZAR!', 'Conectate y comienza a jugar ya!', 'mmquiroga10@gmail.com', [user.email])

    #VARIABLES API
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.verificados.all()
    for user in usuarios:
        plataforma = user.user.last_name
        u1 = user.user.username
        u2 = user.user.first_name
        u1 = u1.replace(" ", "%20")
        u2 = u2.replace(" ", "%20")
        url1 = URL + plataforma + '/' + u1
        url2 = URL + plataforma + '/' + u2
        respuesta_1 = requests.get(url1, headers=headers)
        resultado_1 = respuesta_1.json()
        respuesta_2 = requests.get(url2, headers=headers)
        resultado_2 = respuesta_2.json()
        if 'error' in resultado_1.keys():
            no = no
        else:
            resultado_1 = respuesta_1.json()['lifeTimeStats']
            for r in resultado_1:
                if r['key'] == 'Wins':
                    prewins_1 = r['value']
                if r['key'] == 'Kills':
                    prekills_1 = r['value']
                if r['key'] == 'Matches Played':
                    prepartidas_1 = r['value']
            if 'error' in resultado_2.keys():
                no2 = no2
            else:
                resultado_2 = respuesta_2.json()['lifeTimeStats']
                for r in resultado_2:
                    if r['key'] == 'Wins':
                        prewins_2 = r['value']
                    if r['key'] == 'Kills':
                        prekills_2 = r['value']
                    if r['key'] == 'Matches Played':
                        prepartidas_2 = r['value']
                Perfil.objects.filter(user__username=u1).update(postkills_1=prekills_1, postwins_1=prewins_1, postpartidas_1=prepartidas_1)
                Perfil.objects.filter(user__username=u1).update(postkills_2=prekills_2, postwins_2=prewins_2, postpartidas_2=prepartidas_2)
finalizar_torneo_sin_calculos.short_description = "FINALIZAR SIN CALCULOS"



def finalizar_torneo(modeladmin, request, queryset):
        #VARIABLES API
        URL = "https://api.fortnitetracker.com/v1/profile/"
        headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
        usuarios = Perfil.verificados.all()
        for user in usuarios:
            plataforma = user.user.last_name
            u1 = user.user.username
            u2 = user.user.first_name
            u1 = u1.replace(" ", "%20")
            u2 = u2.replace(" ", "%20")
            url1 = URL + plataforma + '/' + u1
            url2 = URL + plataforma + '/' + u2
            respuesta_1 = requests.get(url1, headers=headers)
            #time.sleep(2)
            resultado_1 = respuesta_1.json()
            respuesta_2 = requests.get(url2, headers=headers)
            #time.sleep(2)
            resultado_2 = respuesta_2.json()
            if 'error' in resultado_1.keys():
                no = no
            else:
                resultado_1 = respuesta_1.json()['lifeTimeStats']
                for r in resultado_1:
                    if r['key'] == 'Wins':
                        postwins_1 = r['value']
                    if r['key'] == 'Kills':
                        postkills_1 = r['value']
                    if r['key'] == 'Matches Played':
                        postpartidas_1 = r['value']
                if 'error' in resultado_2.keys():
                    no2 = no2
                else:
                    resultado_2 = respuesta_2.json()['lifeTimeStats']
                    for r in resultado_2:
                        if r['key'] == 'Wins':
                            postwins_2 = r['value']
                        if r['key'] == 'Kills':
                            postkills_2 = r['value']
                        if r['key'] == 'Matches Played':
                            postpartidas_2 = r['value']
            #PRE Y POST VARIABLES
            postwins_1 = int(postwins_1)
            postwins_2 = int(postwins_2)
            postkills_1 = int(postkills_1)
            postkills_2 = int(postkills_2)
            prekills_1 = user.prekills_1
            prekills_2 = user.prekills_2
            prekills_1 = int(prekills_1)
            prekills_2 = int(prekills_2)
            prewins_1 = user.prewins_1
            prewins_2 = user.prewins_2
            prewins_1 = int(prewins_1)
            prewins_2 = int(prewins_2)
            postpartidas_1 = int(postpartidas_1)
            prepartidas_1 = user.prepartidas_1
            prepartidas_1 = int(prepartidas_1)
            partidas_liga = user.partidas_liga
            partidas_liga = int(partidas_liga)
            kills_liga = user.kills_liga
            kills_liga = int(kills_liga)
            partidas_liga = user.partidas_liga
            partidas_liga = int(partidas_liga)
            #OPERACIONES TORNEO
            wins_1 = postwins_1 - prewins_1
            wins_2 = postwins_2 - prewins_2
            wins_totales = wins_1
            kills_1 = postkills_1 - prekills_1
            kills_2 = postkills_2 - prekills_2
            kills_totales = kills_1 + kills_2
            puntoswins = wins_totales * 15
            puntos = puntoswins + kills_totales
            partidas_totales = postpartidas_1 - prepartidas_1
            #OPERACIONES GENERALES
            pregeneral = user.general
            pregeneral = int(pregeneral)
            nuevogeneral = pregeneral + puntos
            prepartidas_liga = user.partidas_liga
            prepartidas_liga = int(prepartidas_liga)
            postpartidas_liga = prepartidas_liga + partidas_totales
            prekills_liga = user.kills_liga
            prekills_liga = int(prekills_liga)
            postkills_liga = prekills_liga + kills_totales
            km = 0
            if postkills_liga == 0 or postpartidas_liga == 0:
                nola = '0'
            else:
                km = postkills_liga / postpartidas_liga
                km = Decimal(km)
                km = round(km,2)
            Perfil.objects.filter(user__username=u1).update(postkills_1=postkills_1, postwins_1=postwins_1, postpartidas_1=postpartidas_1)
            Perfil.objects.filter(user__username=u1).update(postkills_2=postkills_2, postwins_2=postwins_2, postpartidas_2=postpartidas_2)
            Perfil.objects.filter(user__username=u1).update(puntos=puntos, wins_totales=wins_totales, kills_totales=kills_totales, kd=km, partidas_liga=postpartidas_liga, kills_liga=postkills_liga, general=nuevogeneral)
finalizar_torneo.short_description = "FINALIZAR TORNEO viejo"

class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]
    actions = [resetear_torneo, resetear_todo, mail_comienzo_torneo, comenzar_torneo, finalizar_torneo, finalizar_torneo_sin_calculos]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Perfil)



# Register your models here.
