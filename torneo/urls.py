
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    url(r'^reglas/', views.reglas, name='reglas' ),
    url(r'^premios/', views.premios, name='premios' ),
    #Prueba nueva pagina
    url(r'^test/', views.test, name='test' ),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^fortnite/sistema/', include('fortnite_apps.sistema.urls')),
    url(r'^fortnite/blackpan/', include('fortnite_apps.blackpan.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]

admin.site.site_header = "Administrador LAF"
admin.site.site_title = "Panel de la Liga Argentina de Fortnite"
admin.site.index_title = "Bienvenido!"
