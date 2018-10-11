from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from sistema.models import Perfil
import requests
from decimal import Decimal
from django.core.mail import send_mail
import time
# We should all know what this is used for by now.
from django.core.mail import send_mail
# get_template is what we need for loading up the template for parsing.
from django.template.loader import get_template
# Templates in Django need a "Context" to parse with, so we'll borrow this.
# "Context"'s are really nothing more than a generic dict wrapped up in a
# neat little function call.
from django.template import Context


# Our send_mail call revisited. This time, instead of passing
# a string for the body, we load up a template with get_template()
# and render it with a Context of the variables we want to make available
# to that template.


def mail_prueba_rq():
    equipo = 'hola'
    u1 = 'u1'
    u2 = 'dd'
    send_mail(
        'COMIENZA EL TORNEO!',
        get_template('sistema/email/comenzar.html').render(
            Context({
                'equipo': equipo,
                'u1': cuenta,
                'u2': full_name
            })
        ),
        'ligafortnitearg@gmail.com',
        ['mmquiroga10@gmail.com'],
        fail_silently = True
    )


def comenzar_torneo_rq():
    #ENVIAR MAIL DE COMIENZO
    #for user in User.objects.all():
    #    send_mail('EL TORNEO ACABA DE COMENZAR!', 'Conectate y comienza a jugar ya!', 'mmquiroga10@gmail.com', [user.email])

    #VARIABLES API
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.verificados.order_by('user__date_joined')
    #Perfil.objects.filter(user__last_name='pc', VERIFICACION_2=True).order_by('-puntos')
    for user in usuarios:
        if user.prekills_1 == 0:
            equipo = user.perfil.equipo
            plataforma = user.user.last_name
            cuenta = user.user.username
            cuenta2 = user.user.first_name
            u1 = user.user.username
            u2 = user.user.first_name
            u1 = u1.replace(" ", "%20")
            u2 = u2.replace(" ", "%20")
            url1 = URL + plataforma + '/' + u1
            url2 = URL + plataforma + '/' + u2
            # send_mail(
            #     'Thanks for signing up!',
            #     get_template('sistema/email/comenzar.html').render(
            #         Context({
            #             'equipo': equipo,
            #             'u1': cuenta,
            #             'u2': full_name
            #         })
            #     ),
            #     'ligafortnitearg@gmail.com',
            #     [user.email],
            #     fail_silently = True
            # )
            respuesta_1 = requests.get(url1, headers=headers)
            time.sleep(2)
            resultado_1 = respuesta_1.json()
            respuesta_2 = requests.get(url2, headers=headers)
            time.sleep(2)
            resultado_2 = respuesta_2.json()
            if 'stats' in resultado_1.keys():
                resultado_1 = respuesta_1.json()['stats']
                if 'p10' in resultado_1.keys():
                    prewins_1 = respuesta_1.json()['stats']['p10']['top1']['value']
                    prekills_1 = respuesta_1.json()['stats']['p10']['kills']['value']
                    pretop5_1 = respuesta_1.json()['stats']['p10']['top5']['value']
                    prepartidas_1 = respuesta_1.json()['stats']['p10']['matches']['value']
                    if 'stats' in resultado_2.keys():
                        resultado_2 = respuesta_2.json()['stats']
                        if 'p10' in resultado_2.keys():
                            prewins_2 = respuesta_2.json()['stats']['p10']['top1']['value']
                            prekills_2 = respuesta_2.json()['stats']['p10']['kills']['value']
                            #top2 = respuesta_2.json()['stats']['p10']['top5']['value']
                            prepartidas_2 = respuesta_2.json()['stats']['p10']['matches']['value']
                            Perfil.objects.filter(user__username=cuenta).update(prekills_1=prekills_1, prewins_1=prewins_1, prepartidas_1=prepartidas_1, pretop5_1=pretop5_1, prekills_2=prekills_2, prewins_2=prewins_2, prepartidas_2=prepartidas_2)

def finalizar_torneo_rq():
        #VARIABLES API
        URL = "https://api.fortnitetracker.com/v1/profile/"
        headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
        usuarios = Perfil.verificados.order_by('user__date_joined')
        for user in usuarios:
            if user.prekills_1 != 0:
                if user.postkills_1 == 0:
                    cuenta = user.user.username
                    plataforma = user.user.last_name
                    u1 = user.user.username
                    u2 = user.user.first_name
                    u1 = u1.replace(" ", "%20")
                    u2 = u2.replace(" ", "%20")
                    url1 = URL + plataforma + '/' + u1
                    url2 = URL + plataforma + '/' + u2
                    respuesta_1 = requests.get(url1, headers=headers)
                    time.sleep(2)
                    resultado_1 = respuesta_1.json()
                    respuesta_2 = requests.get(url2, headers=headers)
                    time.sleep(2)
                    resultado_2 = respuesta_2.json()
                    if 'stats' in resultado_1.keys():
                        resultado_1 = respuesta_1.json()['stats']
                        if 'p10' in resultado_1.keys():
                            postwins_1 = respuesta_1.json()['stats']['p10']['top1']['value']
                            postkills_1 = respuesta_1.json()['stats']['p10']['kills']['value']
                            posttop5_1 = respuesta_1.json()['stats']['p10']['top5']['value']
                            postpartidas_1 = respuesta_1.json()['stats']['p10']['matches']['value']
                            if 'stats' in resultado_2.keys():
                                resultado_2 = respuesta_2.json()['stats']
                                if 'p10' in resultado_2.keys():
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
                                    Perfil.objects.filter(user__username=cuenta).update(postkills_1=postkills_1, postwins_1=postwins_1, postpartidas_1=postpartidas_1, posttop5_1=posttop5_1, top5_1=top5_1)
                                    Perfil.objects.filter(user__username=cuenta).update(postkills_2=postkills_2, postwins_2=postwins_2, postpartidas_2=postpartidas_2)
                                    Perfil.objects.filter(user__username=cuenta).update(kills_1=kills_1, wins_1=wins_1, muertes_1=muertes_totales, muertes_2=muertes_totales, kills_2=kills_2, wins_2=wins_2)
                                    Perfil.objects.filter(user__username=cuenta).update(puntos=puntos, wins_totales=wins_totales, kills_totales=kills_totales)
                                    Perfil.objects.filter(user__username=cuenta).update(muertes_totales=muertes_totales)

def mail_comienzo_torneo_rq():
    for user in User.objects.all():
        send_mail('El torneo esta por comenzar!', 'Conectate y preparate!', 'ligafortnitearg@gmail.com', [user.email])

def calcular_puntajes_general_rq():
    usuarios = Perfil.verificados.order_by('user__date_joined')
    for user in usuarios:
        #PUNTOS GENERAL
        u1 = user.user.username
        pregeneral = user.general
        pregeneral = int(pregeneral)
        puntos = user.puntos
        puntos = int(puntos)
        nuevogeneral = pregeneral + puntos
        #KD
        premuertes_liga = user.muertes_liga
        premuertes_liga = int(premuertes_liga)
        muertes_totales = user.muertes_totales
        muertes_totales = int(muertes_totales)
        postmuertes_liga = premuertes_liga + muertes_totales
        prekills_liga = user.kills_liga
        prekills_liga = int(prekills_liga)
        kills_totales = user.kills_totales
        kills_totales = int(kills_totales)
        postkills_liga = prekills_liga + kills_totales
        km = 0
        if postkills_liga == 0 or postmuertes_liga == 0:
            nola = '0'
        else:
            km = postkills_liga / postmuertes_liga
            km = Decimal(km)
            km = round(km,2)

        Perfil.objects.filter(user__username=u1).update(kd=km, general=nuevogeneral, muertes_liga=postmuertes_liga, kills_liga=postkills_liga)
