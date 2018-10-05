from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from sistema.models import Perfil
import requests
from decimal import Decimal
from django.core.mail import send_mail
import time

def comenzar_torneo_rq():
    #ENVIAR MAIL DE COMIENZO
    #for user in User.objects.all():
    #    send_mail('EL TORNEO ACABA DE COMENZAR!', 'Conectate y comienza a jugar ya!', 'mmquiroga10@gmail.com', [user.email])

    #VARIABLES API
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.verificados.all()
    for user in usuarios:
        if user.prekills_1 == 0:
            plataforma = user.user.last_name
            u1 = user.user.username
            u2 = user.user.first_name
            u1 = u1.replace(" ", "%20")
            u2 = u2.replace(" ", "%20")
            url1 = URL + plataforma + '/' + u1
            url2 = URL + plataforma + '/' + u2
            respuesta_1 = requests.get(url1, headers=headers)
            time.sleep(1.5)
            resultado_1 = respuesta_1.json()
            respuesta_2 = requests.get(url2, headers=headers)
            time.sleep(1.5)
            resultado_2 = respuesta_2.json()
            if 'lifeTimeStats' in resultado_1.keys():
                prewins_1 = respuesta_1.json()['stats']['p10']['top1']['value']
                prekills_1 = respuesta_1.json()['stats']['p10']['kills']['value']
                pretop5_1 = respuesta_1.json()['stats']['p10']['top5']['value']
                prepartidas_1 = respuesta_1.json()['stats']['p10']['matches']['value']
                if 'lifeTimeStats' in resultado_2.keys():
                    prewins_2 = respuesta_2.json()['stats']['p10']['top1']['value']
                    prekills_2 = respuesta_2.json()['stats']['p10']['kills']['value']
                    #top2 = respuesta_2.json()['stats']['p10']['top5']['value']
                    prepartidas_2 = respuesta_2.json()['stats']['p10']['matches']['value']
                    Perfil.objects.filter(user__username=u1).update(prekills_1=prekills_1, prewins_1=prewins_1, prepartidas_1=prepartidas_1, pretop5_1=pretop5_1, prekills_2=prekills_2, prewins_2=prewins_2, prepartidas_2=prepartidas_2)
