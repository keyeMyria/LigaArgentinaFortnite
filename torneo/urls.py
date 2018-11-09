
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
    url(r'^premios/', views.premios, name='premios' ),
    url(r'^blackpan/', views.blackpan, name='black_pan' )
    url(r'^blackpan/participantes', views.blackpan_participantes, name='black_pan_participantes' )
    url(r'^blackpan/resultados', views.blackpan_resultados, name='black_pan_resultados' )
    url(r'^blackpan/premios', views.blackpan_premios, name='black_pan_premios' )
    url(r'^blackpan/terminos', views.blackpan_terminos, name='black_pan_terminos' )

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]

admin.site.site_header = "Administrador LAF"
admin.site.site_title = "Panel de la Liga Argentina de Fortnite"
admin.site.index_title = "Bienvenido!"
