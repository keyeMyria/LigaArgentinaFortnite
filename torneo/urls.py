
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^sistema/', include('sistema.urls')),
    url(r'^reglas/', views.reglas, name='reglas' ),
    url(r'^premios/', views.premios, name='premios' )
    url(r'^blackpan/', views.premios, name='black_pan' )

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]

admin.site.site_header = "Administrador LAF"
admin.site.site_title = "Panel de la Liga Argentina de Fortnite"
admin.site.index_title = "Bienvenido!"
