from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from sistema.models import Perfil
import requests
from decimal import Decimal
from django.core.mail import send_mail


class PerfilInline (admin.StackedInline):
    model = Perfil
    can_delete = False

def mail_comienzo_torneo(modeladmin, request, queryset):
    for user in User.objects.all():
        send_mail('El torneo esta por comenzar!', 'Conectate y preparate!', 'mmquiroga10@gmail.com', [user.email])
mail_comienzo_torneo.short_description = "MAIL POR COMENZAR"

def resetear_todo(modeladmin, request, queryset):
    Perfil.objects.update(prekills='0', postkills='0', prewins='0', postwins='0', kills='0', wins='0', puntos='0', general='0', prepartidas='0', postpartidas='0', partidas='0', kd='0')
resetear_todo.short_description = "XXX Resetear TODO XXX"

def resetear_torneo(modeladmin, request, queryset):
    Perfil.objects.update(prekills='0', postkills='0', prewins='0', postwins='0', kills='0', wins='0', puntos='0', prepartidas='0', postpartidas='0', partidas='0', kd='0')
resetear_torneo.short_description = "XXX Resetear torneo XXX"

def comenzar_torneo(modeladmin, request, queryset):
    for user in User.objects.all():
        send_mail('EL TORNEO ACBA DE COMENZAR!', 'Conectate y comienza a jugar ya!', 'mmquiroga10@gmail.com', [user.email])
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.verificados.all()
    for user in usuarios:
        plataforma = user.user.first_name
        nombre = user.user.username
        url1 = URL + plataforma + '/' + nombre
        respuesta = requests.get(url1, headers=headers)
        resultado = respuesta.json()['lifeTimeStats']
        for r in resultado:
            if r['key'] == 'Wins':
                wins = r['value']
            if r['key'] == 'Kills':
                kills = r['value']
            if r['key'] == 'Matches Played':
                partidas = r['value']
        Perfil.objects.filter(user__username=nombre).update(prekills=kills, prewins=wins, prepartidas=partidas)
comenzar_torneo.short_description = "COMENZAR TORNEO"

def finalizar_torneo(modeladmin, request, queryset):
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.verificados.all()
    for user in usuarios:
        plataforma = user.user.first_name
        nombre = user.user.username
        url1 = URL + plataforma + '/' + nombre
        respuesta = requests.get(url1, headers=headers)
        resultado = respuesta.json()['lifeTimeStats']
        for r in resultado:
            if r['key'] == 'Wins':
                wins = r['value']
            if r['key'] == 'Kills':
                kills = r['value']
            if r['key'] == 'Matches Played':
                postpartidas = r['value']
        wins = int(wins)
        kills = int(kills)
        prekills = user.prekills
        prekills = int(prekills)
        prewins = user.prewins
        prewins = int(prewins)
        winstorneo = wins - prewins
        killstorneo = kills - prekills
        puntoswins = winstorneo * 10
        puntos = puntoswins + killstorneo
        pregeneral = user.general
        pregeneral = int(pregeneral)
        nuevogeneral = pregeneral + puntos
        postpartidas = int(postpartidas)
        prepartidas = user.prepartidas
        prepartidas = int(prepartidas)
        partidas = postpartidas - prepartidas
        if partidas == 0:
            km = '0'
        else:
            km = killstorneo / partidas
        km = Decimal(km)
        km = round(km,2)
        Perfil.objects.filter(user__username=nombre).update(postkills=kills, postwins=wins, puntos=puntos, wins=winstorneo, kills=killstorneo, postpartidas=postpartidas, kd=km, partidas=partidas, general=nuevogeneral)
finalizar_torneo.short_description = "FINALIZAR TORNEO"

class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]
    actions = [resetear_torneo, resetear_todo, mail_comienzo_torneo, comenzar_torneo, finalizar_torneo]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Perfil)



# Register your models here.
