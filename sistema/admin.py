from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from sistema.models import Perfil
import requests
from decimal import Decimal
from django.core.mail import send_mail
import time
from .utils import comenzar_torneo_rq, finalizar_torneo_rq, mail_comienzo_torneo_rq, calcular_puntajes_general_rq, mail_prueba_rq, mail_no_verificados_rq, comenzar_torneo_prueba_rq, send_html_email, mail_comienzo_torneo_black_pan_rq,comenzar_torneo_black_pan_rq, finalizar_torneo_black_pan_rq, calcular_puntajes_general_black_pan_rq, comenzar_torneo_prueba_black_pan_rq, comenzar_torneo_prueba_black_pan_GRAPHQL_rq, id_rq
from rq import Queue
from worker import conn
import django_rq
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
q = Queue(connection=conn)

class PerfilInline (admin.StackedInline):
    model = Perfil
    can_delete = False

headers = {"Scout-App": "ae45e214-016c-421c-aef1-35aaa1fe1201"}


def mail_prueba(modeladmin, request, queryset):
    django_rq.enqueue(mail_prueba_rq)
mail_prueba.short_description = "// MAIL PRUEBA //"

def mail_comienzo_torneo(modeladmin, request, queryset):
    django_rq.enqueue(mail_comienzo_torneo_rq)
mail_comienzo_torneo.short_description = "1 - MAIL POR COMENZAR"

def resetear_todo(modeladmin, request, queryset):
    Perfil.objects.update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', general='0', prepartidas_1='0', postpartidas_1='0', muertes_1='0', kd='0')
    Perfil.objects.update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0', muertes_2='0')
    Perfil.objects.update(kills_totales='0', wins_totales='0', kills_liga='0', muertes_liga='0', muertes_totales='0', pretop5_1='0', posttop5_1='0', top5_1='0')
resetear_todo.short_description = "XXX Resetear TODO XXX"

def resetear_torneo(modeladmin, request, queryset):
    Perfil.objects.update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', prepartidas_1='0', postpartidas_1='0')
    Perfil.objects.update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0')
    Perfil.objects.update(wins_totales='0', kills_totales='0', top5_1='0')
resetear_torneo.short_description = "XXX Resetear torneo XXX"

def comenzar_torneo(modeladmin, request, queryset):
    django_rq.enqueue(comenzar_torneo_rq)
comenzar_torneo.short_description = "2 - COMENZAR TORNEO"

def finalizar_torneo(modeladmin, request, queryset):
    django_rq.enqueue(finalizar_torneo_rq)
finalizar_torneo.short_description = "3 - FINALIZAR TORNEO"

def comenzar_torneo_prueba(modeladmin, request, queryset):
    django_rq.enqueue(comenzar_torneo_prueba_rq)
comenzar_torneo_prueba.short_description = "// COMENZAR PRUEBA //"

def calcular_puntajes_general(modeladmin, request, queryset):
    django_rq.enqueue(calcular_puntajes_general_rq)
calcular_puntajes_general.short_description = "4 - CALCULAR GENERALES"

def verificar_usuario(modeladmin, request, queryset):
    def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.scoutsdk.com/graph', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
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
    for user in queryset:
        plataforma = user.last_name
        cuenta = user.username
        u1 = user.username
        u2 = user.first_name
        if plataforma == 'psn':
            plataforma = 'ps4'
        query_u1 = query1 + '"' + plataforma + '"'+ query2 + '"' + u1 + '"' + query3
        query_u2 = query1 + '"' + plataforma + '"'+ query2 + '"' + u2 + '"' + query3
        ID1 = run_query(query_u1) # Execute the query
        ID2 = run_query(query_u2) # Execute the query

        if plataforma == 'ps4':

            ID_test1 = ID1["data"]["players"]["results"][-1]['player']
            if ID_test1:
                ID1 = ID1["data"]["players"]["results"][-1]['player']['playerId']
                Perfil.objects.filter(user__username=cuenta).update(id1=ID1)
            else:
                ID_test1 = ID1["data"]["players"]["results"][-2]['player']
                if ID_test1:
                    ID1 = ID1["data"]["players"]["results"][-2]['player']['playerId']
                    Perfil.objects.filter(user__username=cuenta).update(id1=ID1)
                else:
                    ID_test1 = ID1["data"]["players"]["results"][-1]['player']
                    if ID_test1:
                        ID1 = ID1["data"]["players"]["results"][-1]['player']['playerId']
                        Perfil.objects.filter(user__username=cuenta).update(id1=ID1)
                    else:
                        ID1 = ID1["data"]["players"]["results"][-3]['player']['playerId']
                        Perfil.objects.filter(user__username=cuenta).update(id1=ID1)


            ID_test2 = ID2["data"]["players"]["results"][-1]['player']
            if ID_test2:
                ID2 = ID2["data"]["players"]["results"][-1]['player']['playerId']
                Perfil.objects.filter(user__username=cuenta).update(id2=ID2)
            else:
                ID_test2 = ID2["data"]["players"]["results"][-2]['player']
                if ID_test2:
                    ID2 = ID2["data"]["players"]["results"][-2]['player']['playerId']
                    Perfil.objects.filter(user__username=cuenta).update(id2=ID2)
                else:
                    ID_test2 = ID2["data"]["players"]["results"][-1]['player']
                    if ID_test2:
                        ID2 = ID2["data"]["players"]["results"][-1]['player']['playerId']
                        Perfil.objects.filter(user__username=cuenta).update(id2=ID2)
                    else:
                        ID2 = ID2["data"]["players"]["results"][-3]['player']['playerId']
                        Perfil.objects.filter(user__username=cuenta).update(id2=ID2)



        else:
            ID1 = ID1["data"]["players"]["results"][0]['player']['playerId']
            ID2 = ID2["data"]["players"]["results"][0]['player']['playerId']
            Perfil.objects.filter(user__username=cuenta).update(id1=ID1, id2=ID2)

        user.perfil.id1 = ID1
        user.perfil.id2 = ID2
        user.perfil.VERIFICACION_2 = True
        user.perfil.comentario = ''
        user.save()
        send_mail('TU TEAM YA ESTA VERIFICADO!', 'Completaste el proceso de verificacion. YA ESTAS PARTICIPANDO!', 'ligafortnitearg@gmail.com', [user.email])
verificar_usuario.short_description = "// VERIFICAR USUARIO //"

def mail_no_verificados(modeladmin, request, queryset):
    django_rq.enqueue(mail_no_verificados_rq)
mail_no_verificados.short_description = "// MAIL A LOS NO VERIFICADOS //"

def usuarios_mal(modeladmin, request, queryset):
    for user in queryset:
        user.perfil.comentario = 'USUARIO NO EXISTE / PLATAFORMA'
        user.perfil.VERIFICACION_2=False
        user.save()
        u1 = user.username
        u2 = user.first_name
        equipo = user.perfil.equipo
        emails = [user.email]
        context = {
            'u1': u1,
            'u2': u2,
            'equipo': equipo
        }
        send_html_email(emails, subject='Tenemos problemas para verificar sus usuarios de Epic', template_name='sistema/email/usuarios_mal.html', context=context, sender="ligafortnitearg@gmail.com")
usuarios_mal.short_description = "// USUARIOS MAL / PLATAFORMA //"

def id_mal(modeladmin, request, queryset):
    for user in queryset:
        user.perfil.id1 = ''
        user.perfil.id2 = ''
        user.save()
id_mal.short_description = "// ID MAL //"

def id(modeladmin, request, queryset):
    django_rq.enqueue(id_rq)
id.short_description = "/////////// ID TODOS"
#BLACK PAN importar funciones rq de utils despues de creearlas

def mail_comienzo_torneo_black_pan(modeladmin, request, queryset):
    django_rq.enqueue(mail_comienzo_torneo_black_pan_rq)
mail_comienzo_torneo_black_pan.short_description = "1BP - MAIL POR COMENZAR"

def comenzar_torneo_black_pan(modeladmin, request, queryset):
    django_rq.enqueue(comenzar_torneo_black_pan_rq)
comenzar_torneo_black_pan.short_description = "2BP - COMENZAR TORNEO"

def finalizar_torneo_black_pan(modeladmin, request, queryset):
    django_rq.enqueue(finalizar_torneo_black_pan_rq)
finalizar_torneo_black_pan.short_description = "3BP - FINALIZAR TORNEO"

def calcular_puntajes_general_black_pan(modeladmin, request, queryset):
    django_rq.enqueue(calcular_puntajes_general_black_pan_rq)
calcular_puntajes_general_black_pan.short_description = "4BP - CALCULAR GENERALES"

def comenzar_torneo_prueba_black_pan(modeladmin, request, queryset):
    django_rq.enqueue(comenzar_torneo_prueba_black_pan_rq)
comenzar_torneo_prueba_black_pan.short_description = "5BP - // COMENZAR PRUEBA BP //"

def comenzar_torneo_prueba_black_pan_GRAPHQL(modeladmin, request, queryset):
    django_rq.enqueue(comenzar_torneo_prueba_black_pan_GRAPHQL_rq)
comenzar_torneo_prueba_black_pan_GRAPHQL.short_description = "6BP - // PRUEBA GRAPHQL //"

def resetear_todo_black_pan(modeladmin, request, queryset):
    Perfil.objects.filter(black_pan='SI').update(prekills_1='0', postkills_1='0', prewins_1='0', postwins_1='0', kills_1='0', wins_1='0', puntos='0', general='0', prepartidas_1='0', postpartidas_1='0', muertes_1='0', kd='0')
    Perfil.objects.filter(black_pan='SI').update(prekills_2='0', postkills_2='0', prewins_2='0', postwins_2='0', kills_2='0', wins_2='0', prepartidas_2='0', postpartidas_2='0', muertes_2='0')
    Perfil.objects.filter(black_pan='SI').update(kills_totales='0', wins_totales='0', kills_liga='0', muertes_liga='0', muertes_totales='0', pretop5_1='0', posttop5_1='0', top5_1='0')
resetear_todo_black_pan.short_description = "6BP - XXX Resetear TODO XXX"

class MyArticleAdminForm(forms.ModelForm):
    def clean_username(self):
        # do something that validates your data
        return user

class MyUserChangeForm(forms.ModelForm):
   class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )
        def clean(self):
            username = username

class MyUserCreateForm(forms.ModelForm):
   class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )
        def clean(self):
            username = self.cleaned_data.get('username')



class UserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreateForm
    inlines = [PerfilInline]
    list_display = ( 'equipo', 'usuario1', 'usuario2', 'plataforma', 'email', 'comentario', 'ver', 'black_pan', 'prekills', 'postkills', 'id_epic1', 'id_epic2')

    def ver(self, obj):
        return obj.perfil.VERIFICACION_2
    ver.boolean = True
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
    def black_pan(self, obj):
        return obj.perfil.black_pan
    def id_epic1(self, obj):
        return obj.perfil.id1
    def id_epic2(self, obj):
        return obj.perfil.id2

    #get_author.short_description = 'Author'
    #get_author.admin_order_field = 'book__author'

    ordering = ('-date_joined', )
    list_filter = ('perfil__VERIFICACION_2', 'last_name', 'perfil__black_pan')
    actions = [resetear_torneo, resetear_todo, mail_comienzo_torneo, comenzar_torneo, finalizar_torneo, calcular_puntajes_general, verificar_usuario, usuarios_mal, comenzar_torneo_prueba, mail_no_verificados, mail_prueba, mail_comienzo_torneo_black_pan, comenzar_torneo_black_pan, finalizar_torneo_black_pan, calcular_puntajes_general_black_pan, comenzar_torneo_prueba_black_pan, resetear_todo_black_pan, comenzar_torneo_prueba_black_pan_GRAPHQL, id, id_mal]



admin.site.unregister(User)
admin.site.register(User, UserAdmin)




# Register your models here.
