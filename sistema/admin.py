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
    Perfil.objects.update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', general='0', prepartidas_1='0', postpartidas_1='0', muertes_1='0', kd='0')
    Perfil.objects.update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0', muertes_2='0')
    Perfil.objects.update(kills_totales='0', wins_totales='0', kills_liga='0', muertes_liga='0', muertes_totales='0', pretop5_1='0', posttop5_1='0', top5_1='0')
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
    URL_id = "https://fortnite-public-api.theapinetwork.com/prod09/users/id"
    URL_stats = 'https://fortnite-public-api.theapinetwork.com/prod09/users/public/br_stats'
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Authorization': "3870d925f574303458005063b9ef7e31"
        }
    usuarios = Perfil.verificados.all()
    for user in usuarios:
        if user.prekills_1 == 0:
            plataforma = user.user.last_name
            u1 = user.user.username
            u2 = user.user.first_name
            u1 = u1.replace(" ", "%20")
            u2 = u2.replace(" ", "%20")
            payload_id_1 = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n" + u1 + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
            payload_id_2 = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n" + u2 + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
            ID_1 = requests.request("POST", URL_id, data=payload_id_1, headers=headers)
            ID_1_ = ID_1.json()
            ID_2 = requests.request("POST", URL_id, data=payload_id_2, headers=headers)
            ID_2_ = ID_2.json()
            if 'uid' in ID_1_.keys():
                ID_1 = ID_1.json()['uid']
                payload_stats_1 = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"user_id\"\r\n\r\n" + ID_1 + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"platform\"\r\n\r\n" + plataforma +  "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"window\"\r\n\r\nalltime\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
                STATS_1 = requests.request("POST", URL_stats, data=payload_stats_1, headers=headers)
                STATS_1_ = STATS_1.json()
                if 'username' in STATS_1_.keys():
                    prewins_1 = STATS_1.json()['stats']['placetop1_duo']
                    prekills_1 = STATS_1.json()['stats']['kills_duo']
                    pretop5_1 = STATS_1.json()['stats']['placetop5_duo']
                    prepartidas_1 = STATS_1.json()['stats']['matchesplayed_duo']
                    if 'uid' in ID_2_.keys():
                        ID_2 = ID_2.json()['uid']
                        payload_stats_2 = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"user_id\"\r\n\r\n" + ID_2 + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"platform\"\r\n\r\n" + plataforma +  "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"window\"\r\n\r\nalltime\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
                        STATS_2 = requests.request("POST", URL_stats, data=payload_stats_2, headers=headers)
                        STATS_2_ = STATS_2.json()
                        if 'username' in STATS_2_.keys():
                            prewins_2 = STATS_2.json()['stats']['placetop1_duo']
                            prekills_2 = STATS_2.json()['stats']['kills_duo']
                            pretop5_2 = STATS_2.json()['stats']['placetop5_duo']
                            prepartidas_2 = STATS_2.json()['stats']['matchesplayed_duo']
                        Perfil.objects.filter(user__username=u1).update(prekills_1=prekills_1, prewins_1=prewins_1, prepartidas_1=prepartidas_1, pretop5_1=pretop5_1, prekills_2=prekills_2, prewins_2=prewins_2, prepartidas_2=prepartidas_2)
comenzar_torneo.short_description = "COMENZAR TORNEO"


def finalizar_torneo(modeladmin, request, queryset):
        #VARIABLES API
        URL = "https://api.fortnitetracker.com/v1/profile/"
        headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
        usuarios = Perfil.verificados.all()
        for user in usuarios:
            if user.prekills_1 != 0:
                if user.postkills_1 == 0:
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
                    if 'lifeTimeStats' in resultado_1.keys():
                        postwins_1 = respuesta_1.json()['stats']['p10']['top1']['value']
                        postkills_1 = respuesta_1.json()['stats']['p10']['kills']['value']
                        posttop5_1 = respuesta_1.json()['stats']['p10']['top5']['value']
                        postpartidas_1 = respuesta_1.json()['stats']['p10']['matches']['value']
                        if 'lifeTimeStats' in resultado_2.keys():
                            postwins_2 = respuesta_2.json()['stats']['p10']['top1']['value']
                            postkills_2 = respuesta_2.json()['stats']['p10']['kills']['value']
                            #top5 = respuesta_2.json()['stats']['p10']['top5']['value']
                            postpartidas_2 = respuesta_2.json()['stats']['p10']['matches']['value']
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
                            postpartidas_2 = int(postpartidas_2)
                            prepartidas_1 = user.prepartidas_1
                            prepartidas_1 = int(prepartidas_1)
                            prepartidas_2 = user.prepartidas_2
                            prepartidas_2 = int(prepartidas_2)
                            muertes_liga = user.muertes_liga
                            partidas_liga = int(muertes_liga)
                            kills_liga = user.kills_liga
                            kills_liga = int(kills_liga)
                            partidas_liga = user.muertes_liga
                            partidas_liga = int(muertes_liga)
                            #PRUEBA TOP5
                            pretop5_1 = user.pretop5_1
                            pretop5_1 = int(pretop5_1)
                            posttop5_1 = int(posttop5_1)
                            top5_1 = posttop5_1 - pretop5_1
                            #OPERACIONES TORNEO
                            wins_1 = postwins_1 - prewins_1
                            wins_2 = postwins_2 - prewins_2
                            wins_totales = wins_1
                            kills_1 = postkills_1 - prekills_1
                            kills_2 = postkills_2 - prekills_2
                            kills_totales = kills_1 + kills_2
                            puntoswins = wins_totales * 15
                            puntostop5 = top5_1 * 4
                            puntos = puntoswins + kills_totales + puntostop5
                            muertes_1 = postpartidas_1 - prepartidas_1 - wins_totales
                            muertes_2 = postpartidas_2 - prepartidas_2 - wins_totales
                            muertes_totales = 0
                            if muertes_1 != 0:
                                muertes_totales = muertes_1
                            else:
                                muertes_totales = muertes_2
                            #OPERACIONES GENERALES
                            pregeneral = user.general
                            pregeneral = int(pregeneral)
                            nuevogeneral = pregeneral + puntos
                            premuertes_liga = user.muertes_liga
                            premuertes_liga = int(premuertes_liga)
                            postmuertes_liga = premuertes_liga + muertes_totales
                            prekills_liga = user.kills_liga
                            prekills_liga = int(prekills_liga)
                            postkills_liga = prekills_liga + kills_totales
                            km = 0
                            if postkills_liga == 0 or postmuertes_liga == 0:
                                nola = '0'
                            else:
                                km = postkills_liga / postmuertes_liga
                                km = Decimal(km)
                                km = round(km,2)
                            Perfil.objects.filter(user__username=u1).update(postkills_1=postkills_1, postwins_1=postwins_1, postpartidas_1=postpartidas_1, posttop5_1=posttop5_1, top5_1=top5_1)
                            Perfil.objects.filter(user__username=u1).update(postkills_2=postkills_2, postwins_2=postwins_2, postpartidas_2=postpartidas_2)
                            Perfil.objects.filter(user__username=u1).update(kills_1=kills_1, wins_1=wins_1, muertes_1=muertes_totales, muertes_2=muertes_totales, kills_2=kills_2, wins_2=wins_2)
                            Perfil.objects.filter(user__username=u1).update(puntos=puntos, wins_totales=wins_totales, kills_totales=kills_totales, kd=km, kills_liga=postkills_liga, general=nuevogeneral)
                            Perfil.objects.filter(user__username=u1).update(muertes_liga=postmuertes_liga, muertes_totales=muertes_totales)
finalizar_torneo.short_description = "FINALIZAR TORNEO"

def comentario_1(modeladmin, request, queryset):
    com = '-'
    Perfil.objects.update(comentario=com)
comentario_1.short_description = "comentario"

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
    actions = [resetear_torneo, resetear_todo, mail_comienzo_torneo, comenzar_torneo, finalizar_torneo, comentario_1]

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipo', 'VERIFICACION_2')
    ordering = ('VERIFICACION_2', )
    actions = [resetear_torneo, resetear_todo, mail_comienzo_torneo, comenzar_torneo, finalizar_torneo]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Perfil, PerfilAdmin)



# Register your models here.
