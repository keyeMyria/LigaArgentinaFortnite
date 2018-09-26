from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
# Create your models here.

class PerfilManager(models.Manager):
    def get_queryset(self):
        return super(PerfilManager, self).get_queryset().filter(VERIFICACION=True)


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    VERIFICACION = models.BooleanField(default=False)
    prekills = models.IntegerField(blank=True, default=0)
    postkills = models.IntegerField(blank=True, default=0)
    kills = models.IntegerField(blank=True, default=0)
    prewins = models.IntegerField(blank=True, default=0)
    postwins = models.IntegerField(blank=True, default=0)
    wins = models.IntegerField(blank=True, default=0)
    prepartidas = models.IntegerField(blank=True, default=0)
    postpartidas = models.IntegerField(blank=True, default=0)
    partidas = models.IntegerField(blank=True, default=0)
    kd = models.CharField(max_length=4, blank=True, default=0)
    puntos = models.IntegerField(blank=True, default=0)
    general = models.IntegerField(blank=True, default=0)
    equipo = models.CharField(max_length=20, blank=True, default=0)



    objects = models.Manager()
    verificados = PerfilManager()

    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()
