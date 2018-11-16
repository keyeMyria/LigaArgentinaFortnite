from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from sistema.models import Perfil
import requests
from decimal import Decimal
import time
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings

# SCOUT API HEADERS

headers_token = {'Content-Type':'application/x-www-form-urlencoded'}
API_ENDPOINT = "https://api.scoutsdk.com/connect/token"
data = {'grant_type': 'client_credentials',
        'client_id': 'ae45e214-016c-421c-aef1-35aaa1fe1201',
        'client_secret': '3b5efcc90bb3438e11cf49be6837854c7ba509fbb5eaa8374802326656476920',
        'scope': 'public.read'
        }


def id_rq():
    usuarios = Perfil.verificados.order_by('user__date_joined')
    r = requests.post(url = API_ENDPOINT, headers=headers_token, data=data)
    hola = r.json()
    token = hola['access_token']
    bearer = 'Bearer ' + token
    headers = {"Authorization": bearer ,"Scout-App": "ae45e214-016c-421c-aef1-35aaa1fe1201"}
    def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.scoutsdk.com/graph', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    for user in usuarios:
        if user.id1 == '':
            plataforma = user.user.last_name
            cuenta = user.user.username
            cuenta2 = user.user.first_name
            u1 = user.user.username
            u2 = user.user.first_name

            if plataforma == 'psn':
                plataforma = 'ps4'

            query1 = """
            {
              players(title: "fortnite", platform: "epic", console: """

            query2 = """ identifier: """


            query3 = """) {
                results {
                  player {
                    playerId
                    handle
                  }
                  persona {
                    id
                    handle
                  }
                }
              }
            }
            """
            query_u1 = query1 + '"' + plataforma + '"'+ query2 + '"' + u1 + '"' + query3
            query_u2 = query1 + '"' + plataforma + '"'+ query2 + '"' + u2 + '"' + query3
            ID1 = run_query(query_u1) # Execute the query
            ID2 = run_query(query_u2) # Execute the query

            ID1 = ID1["data"]["players"]["results"][-1]['player']['playerId']
            ID2 = ID2["data"]["players"]["results"][-1]['player']['playerId']

            # if ID1 != "{'data': {'players': {'results': []}}}" or ID2 != "{'data': {'players': {'results': []}}}":
            #     if plataforma == 'psn':
            #         ID1 = ID1["data"]["players"]["results"][0]['player']['playerId']
            #         ID2 = ID2["data"]["players"]["results"][0]['player']['playerId']
            #     else:
            #         ID1 = ID1["data"]["players"]["results"][0]['persona']['id']
            #         ID2 = ID2["data"]["players"]["results"][0]['persona']['id']
            Perfil.objects.filter(user__username=cuenta).update(id1=ID1, id2=ID2)


# FUNCIONES PARA LLAMRA DESDE ADMIN
def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    msg_html = render_to_string(template_name, context)
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()

def mail_prueba_rq():
    equipo = 'hola'
    kills_totales = 'u1'
    wins_totales = 'dd'
    top5_1 = 'kk'
    emails = ['mmquiroga10@gmail.com']
    context = {
        'equipo': equipo,
        'kills': kills_totales,
        'wins': wins_totales,
        'tops5': top5_1
    }
    send_html_email(emails, subject='EL TORNEO ACABA DE FINALIZAR! MIRA TUS RESULTADOS!', template_name='sistema/email/por_comenzar.html', context=context, sender="ligafortnitearg@gmail.com")

def comenzar_torneo_rq():
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.verificados.order_by('user__date_joined')
    #Perfil.objects.filter(user__last_name='pc', VERIFICACION_2=True).order_by('-puntos')
    for user in usuarios:
        if user.prekills_1 == 0:
            equipo = user.equipo
            plataforma = user.user.last_name
            cuenta = user.user.username
            cuenta2 = user.user.first_name
            u1 = user.user.username
            u2 = user.user.first_name
            u1 = u1.replace(" ", "%20")
            u2 = u2.replace(" ", "%20")
            url1 = URL + plataforma + '/' + u1
            url2 = URL + plataforma + '/' + u2
            # MAIL COMIENZO TORNEO
            emails = [user.user.email]
            context = {
                'equipo': equipo,
                'u1': cuenta,
                'u2': cuenta2
            }
            send_html_email(emails, subject='COMIENZA EL TORNEO! A JUGAR!', template_name='sistema/email/comenzar.html', context=context, sender="ligafortnitearg@gmail.com")
            # API REQUESTS
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
                    equipo = user.equipo
                    cuenta = user.user.username
                    plataforma = user.user.last_name
                    u1 = user.user.username
                    u2 = user.user.first_name
                    u1 = u1.replace(" ", "%20")
                    u2 = u2.replace(" ", "%20")
                    url1 = URL + plataforma + '/' + u1
                    url2 = URL + plataforma + '/' + u2
                    # API REQUESTS
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
                                    # MAIL FINALIZAR TORNEO
                                    emails = [user.user.email]
                                    context = {
                                        'equipo': equipo,
                                        'kills': kills_totales,
                                        'wins': wins_totales,
                                        'tops5': top5_1
                                    }
                                    send_html_email(emails, subject='EL TORNEO ACABA DE FINALIZAR! MIRA TUS RESULTADOS!', template_name='sistema/email/finalizar.html', context=context, sender="ligafortnitearg@gmail.com")

def comenzar_torneo_prueba_rq():
    usuarios = Perfil.verificados.order_by('-user__date_joined')
    r = requests.post(url = API_ENDPOINT, headers=headers_token, data=data)
    hola = r.json()
    token = hola['access_token']
    bearer = 'Bearer ' + token
    headers = {"Authorization": bearer ,"Scout-App": "ae45e214-016c-421c-aef1-35aaa1fe1201"}
    def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.scoutsdk.com/graph', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    for user in usuarios:
        if user.prekills_1 == 0:
            equipo = user.equipo
            cuenta = user.user.username
            cuenta2 = user.user.first_name
            u1 = user.user.username
            u2 = user.user.first_name
            ID1 = user.id1
            ID2 = user.id2

            query_stats1 = """
            {
              player(title: "fortnite", id: """

            query_stats2 = """, segment: "p10.br.m0.alltime") {
                id
                metadata {
                  key
                  name
                  value
                  displayValue
                }
                stats {
                  metadata {
                    key
                    name
                    isReversed
                  }
                  value
                  displayValue
                }
                segments {
                  metadata {
                    key
                    name
                    value
                    displayValue
                  }
                  stats {
                    metadata {
                      key
                      name
                      isReversed
                    }
                    value
                    displayValue
                  }
                }
              }
            }
            """
            query_u1 = query_stats1 + '"' + ID1 + '"' + query_stats2
            query_u2 = query_stats1 + '"' + ID2 + '"' + query_stats2
            stats1 = run_query(query_u1)
            stats2 = run_query(query_u2)
            # if 'stats' in stats1.keys():
            top5 = stats1
            stats1 = stats1['data']['player']['segments']
            if stats1:
                prekills_1 = stats1[0]['stats'][0]['value']
                prewins_1 = stats1[0]['stats'][3]['value']
                pretop5_1 = top5['data']['player']['stats'][5]['value']
                prepartidas_1 = stats1[0]['stats'][2]['value']
                Perfil.objects.filter(user__username=cuenta).update(prekills_1=prekills_1, prewins_1=prewins_1, prepartidas_1=prepartidas_1, pretop5_1=pretop5_1)

            stats2 = stats2['data']['player']['segments']
            if stats2:
                prekills_2 = stats2[0]['stats'][0]['value']
                prewins_2 = stats2[0]['stats'][3]['value']
                prepartidas_2 = stats2[0]['stats'][2]['value']
                Perfil.objects.filter(user__username=cuenta).update(prekills_2=prekills_2, prewins_2=prewins_2, prepartidas_2=prepartidas_2)


def mail_comienzo_torneo_rq():
    usuarios = Perfil.verificados.order_by('user__date_joined')
    for user in usuarios:
        equipo = 'hola'
        emails = [user.user.email]
        context = {
            'equipo': equipo
        }
        send_html_email(emails, subject='EL TORNEO ESTA POR COMENZAR!', template_name='sistema/email/por_comenzar.html', context=context, sender="ligafortnitearg@gmail.com")

def mail_no_verificados_rq():
    usuarios = Perfil.noverificados.order_by('user__date_joined')
    for user in usuarios:
        equipo = 'hola'
        emails = [user.user.email]
        context = {
            'equipo': equipo
        }
        send_html_email(emails, subject='Todavia puedes corregir tu inscripcion!', template_name='sistema/email/no_verificados.html', context=context, sender="ligafortnitearg@gmail.com")

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

#black_pan

def mail_comienzo_torneo_black_pan_rq():
    usuarios = Perfil.black_pan_verificados.order_by('user__date_joined')
    for user in usuarios:
        equipo = 'hola'
        emails = [user.user.email]
        context = {
            'equipo': equipo
        }
        send_html_email(emails, subject='EL TORNEO ESTA POR COMENZAR!', template_name='sistema/email/por_comenzar.html', context=context, sender="ligafortnitearg@gmail.com")

def comenzar_torneo_black_pan_rq():
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.black_pan_verificados.order_by('user__date_joined')
    #Perfil.objects.filter(user__last_name='pc', VERIFICACION_2=True).order_by('-puntos')
    for user in usuarios:
        if user.prekills_1 == 0:
            equipo = user.equipo
            plataforma = user.user.last_name
            cuenta = user.user.username
            cuenta2 = user.user.first_name
            u1 = user.user.username
            u2 = user.user.first_name
            u1 = u1.replace(" ", "%20")
            u2 = u2.replace(" ", "%20")
            url1 = URL + plataforma + '/' + u1
            url2 = URL + plataforma + '/' + u2
            # MAIL COMIENZO TORNEO
            emails = [user.user.email]
            context = {
                'equipo': equipo,
                'u1': cuenta,
                'u2': cuenta2
            }
            send_html_email(emails, subject='COMIENZA EL TORNEO! A JUGAR!', template_name='sistema/email/comenzar.html', context=context, sender="ligafortnitearg@gmail.com")
            # API REQUESTS
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

def finalizar_torneo_black_pan_rq():
        #VARIABLES API
        URL = "https://api.fortnitetracker.com/v1/profile/"
        headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
        usuarios = Perfil.black_pan_verificados.order_by('user__date_joined')
        for user in usuarios:
            if user.prekills_1 != 0:
                if user.postkills_1 == 0:
                    equipo = user.equipo
                    cuenta = user.user.username
                    plataforma = user.user.last_name
                    u1 = user.user.username
                    u2 = user.user.first_name
                    u1 = u1.replace(" ", "%20")
                    u2 = u2.replace(" ", "%20")
                    url1 = URL + plataforma + '/' + u1
                    url2 = URL + plataforma + '/' + u2
                    # API REQUESTS
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
                                    # MAIL FINALIZAR TORNEO
                                    emails = [user.user.email]
                                    context = {
                                        'equipo': equipo,
                                        'kills': kills_totales,
                                        'wins': wins_totales,
                                        'tops5': top5_1
                                    }
                                    send_html_email(emails, subject='EL TORNEO ACABA DE FINALIZAR! MIRA TUS RESULTADOS!', template_name='sistema/email/finalizar.html', context=context, sender="ligafortnitearg@gmail.com")

def calcular_puntajes_general_black_pan_rq():
    usuarios = Perfil.black_pan_verificados.order_by('user__date_joined')
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

def comenzar_torneo_prueba_black_pan_rq():
    URL = "https://api.fortnitetracker.com/v1/profile/"
    headers = {'TRN-Api-Key':'f22aa3c4-fb80-4658-9e5b-6b1ec7708b84'}
    usuarios = Perfil.black_pan_verificados.order_by('user__date_joined')
    #Perfil.objects.filter(user__last_name='pc', VERIFICACION_2=True).order_by('-puntos')
    for user in usuarios:
        if user.prekills_1 == 0:
            equipo = user.equipo
            plataforma = user.user.last_name
            cuenta = user.user.username
            cuenta2 = user.user.first_name
            u1 = user.user.username
            u2 = user.user.first_name
            u1 = u1.replace(" ", "%20")
            u2 = u2.replace(" ", "%20")
            url1 = URL + plataforma + '/' + u1
            url2 = URL + plataforma + '/' + u2
            # MAIL COMIENZO TORNEO
            # emails = [user.user.email]
            # context = {
            #     'equipo': equipo,
            #     'u1': cuenta,
            #     'u2': cuenta2
            # }
            # send_html_email(emails, subject='COMIENZA EL TORNEO! A JUGAR!', template_name='sistema/email/comenzar.html', context=context, sender="ligafortnitearg@gmail.com")
            # API REQUESTS
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

def comenzar_torneo_prueba_black_pan_GRAPHQL_rq():
    usuarios = Perfil.black_pan_verificados.order_by('user__date_joined')
    r = requests.post(url = API_ENDPOINT, headers=headers_token, data=data)
    hola = r.json()
    token = hola['access_token']
    bearer = 'Bearer ' + token
    headers = {"Authorization": bearer ,"Scout-App": "ae45e214-016c-421c-aef1-35aaa1fe1201"}
    def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.scoutsdk.com/graph', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    for user in usuarios:
        if user.prekills_1 == 0:
            equipo = user.equipo
            cuenta = user.user.username
            cuenta2 = user.user.first_name
            u1 = user.user.username
            u2 = user.user.first_name
            ID1 = user.id1
            ID2 = user.id2

            query_stats1 = """
            {
              player(title: "fortnite", id: """

            query_stats2 = """, segment: "p10.br.m0.alltime") {
                id
                metadata {
                  key
                  name
                  value
                  displayValue
                }
                stats {
                  metadata {
                    key
                    name
                    isReversed
                  }
                  value
                  displayValue
                }
                segments {
                  metadata {
                    key
                    name
                    value
                    displayValue
                  }
                  stats {
                    metadata {
                      key
                      name
                      isReversed
                    }
                    value
                    displayValue
                  }
                }
              }
            }
            """
            query_u1 = query_stats1 + '"' + ID1 + '"' + query_stats2
            query_u2 = query_stats1 + '"' + ID2 + '"' + query_stats2
            stats1 = run_query(query_u1)
            stats2 = run_query(query_u2)
            prekills_1 = stats1['data']['player']['segments'][0]['stats'][0]['value']
            prewins_1 = stats1['data']['player']['segments'][0]['stats'][3]['value']
            pretop5_1 = stats1['data']['player']['stats'][5]['value']
            prepartidas_1 = stats1['data']['player']['segments'][0]['stats'][2]['value']
            prekills_2 = stats2['data']['player']['segments'][0]['stats'][0]['value']
            prewins_2 = stats2['data']['player']['segments'][0]['stats'][3]['value']
            prepartidas_2 = stats2['data']['player']['segments'][0]['stats'][2]['value']
            Perfil.objects.filter(user__username=cuenta).update(prekills_1=prekills_1, prewins_1=prewins_1, prepartidas_1=prepartidas_1, pretop5_1=pretop5_1, prekills_2=prekills_2, prewins_2=prewins_2, prepartidas_2=prepartidas_2)
