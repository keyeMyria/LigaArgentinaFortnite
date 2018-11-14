from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from django.core.validators import RegexValidator

# Create your models here.

class PerfilManager(models.Manager):
    def get_queryset(self):
        return super(PerfilManager, self).get_queryset().filter(VERIFICACION_2=True)

class PerfilManagerNO(models.Manager):
    def get_queryset(self):
        return super(PerfilManagerNO, self).get_queryset().filter(VERIFICACION_2=False)

class PerfilManagerBLACK(models.Manager):
    def get_queryset(self):
        return super(PerfilManagerBLACK, self).get_queryset().filter(black_pan='SI', VERIFICACION_2=True)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    VERIFICACION_1 = models.BooleanField(default=False)
    VERIFICACION_2 = models.BooleanField(default=False)
#USUARIO 1
    prekills_1 = models.IntegerField(blank=True, default=0)
    postkills_1 = models.IntegerField(blank=True, default=0)
    kills_1 = models.IntegerField(blank=True, default=0)
    prewins_1 = models.IntegerField(blank=True, default=0)
    postwins_1 = models.IntegerField(blank=True, default=0)
    wins_1 = models.IntegerField(blank=True, default=0)
    #PRUEBA TOP 5
    pretop5_1 = models.IntegerField(blank=True, default=0)
    posttop5_1 = models.IntegerField(blank=True, default=0)
    top5_1 = models.IntegerField(blank=True, default=0)
    #FIN PRUEBA TOP 5
    prepartidas_1 = models.IntegerField(blank=True, default=0)
    postpartidas_1 = models.IntegerField(blank=True, default=0)
    muertes_1 = models.IntegerField(blank=True, default=0)
    twitch_1 = models.CharField(max_length=20, blank=True, default='')
#USUARIO 2
    prekills_2 = models.IntegerField(blank=True, default=0)
    postkills_2 = models.IntegerField(blank=True, default=0)
    kills_2 = models.IntegerField(blank=True, default=0)
    prewins_2 = models.IntegerField(blank=True, default=0)
    postwins_2 = models.IntegerField(blank=True, default=0)
    wins_2 = models.IntegerField(blank=True, default=0)
    prepartidas_2 = models.IntegerField(blank=True, default=0)
    postpartidas_2 = models.IntegerField(blank=True, default=0)
    muertes_2 = models.IntegerField(blank=True, default=0)
    twitch_2 = models.CharField(max_length=20, blank=True, default='')
#GENERAL
    muertes_totales = models.CharField(max_length=200, blank=True, default=0)
    kills_totales = models.CharField(max_length=200, blank=True, default=0)
    wins_totales = models.CharField(max_length=10, blank=True, default=0)
    kills_liga = models.CharField(max_length=200, blank=True, default=0)
    muertes_liga = models.CharField(max_length=200, blank=True, default=0)
    kd = models.CharField(max_length=200, blank=True, default=0)
    puntos = models.IntegerField(blank=True, default=0)
    general = models.IntegerField(blank=True, default=0)
    equipo = models.CharField(max_length=20, blank=True, default=0)
    comentario = models.CharField(max_length=100, blank=True)
#BLACK PAN
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El telefono tiene que ser ingresado con el formato: '+999999999'")
    telefono = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    black_pan = models.CharField(max_length=100, blank=True, default='NO')
    id1 = models.CharField(max_length=100, blank=True)
    id2 = models.CharField(max_length=100, blank=True)
#MANAGERS
    objects = models.Manager()
    verificados = PerfilManager()
    noverificados = PerfilManagerNO()
    black_pan_verificados = PerfilManagerBLACK()

    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()
