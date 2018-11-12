from django import forms
from . import models


class Inscripcion(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = []

class SignupForm(forms.Form):
    black_pan = forms.ChoiceField(label='Soy de Cordoba y quiro participar del torneo BLACK PAN', choices= ( ('SI', 'SI'), ('NO', 'NO'), ) ,widget=forms.Select(attrs={ 'class': 'input','autofocus': 'autofocus'}))
    first_name = forms.CharField(max_length=30, label='Segundo Participante (USUARIO DE EPIC GAMES, NO PSN)', required=True, widget=forms.TextInput(attrs={ 'class': 'input' ,'placeholder':('Usuario de Epic del segundo participante'),'autofocus': 'autofocus'}))
    last_name = forms.ChoiceField(label='Plataforma ( PC o PSN )', choices= ( ('pc', 'pc'), ('psn', 'psn'), ) ,widget=forms.Select(attrs={ 'class': 'input' ,'placeholder':('pc, ps4 (minusculas)'),'autofocus': 'autofocus'}))
    equipo = forms.CharField(max_length=30, label='Nombre del Equipo', required=True, widget=forms.TextInput(attrs={ 'class': 'input' ,'placeholder':('Equipo'),'autofocus': 'autofocus'}))
    twitch_1 = forms.CharField(max_length=30, label='Twitch del primer participante (no obligatorio)', required=False, widget=forms.TextInput(attrs={ 'class': 'input' ,'placeholder':('Usuario de Twitch'),'autofocus': 'autofocus'}))
    twitch_2 = forms.CharField(max_length=30, label='Twitch del segundo participante (no obligatorio)', required=False, widget=forms.TextInput(attrs={ 'class': 'input' ,'placeholder':('Usuario de Twitch'),'autofocus': 'autofocus'}))
    telefono = forms.IntegerField(label='Telefono de contacto (obligatorio)', required=True, widget=forms.TextInput(attrs={ 'class': 'input' ,'placeholder':('Telefono'),'autofocus': 'autofocus'}))


    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.perfil.equipo = self.cleaned_data['equipo']
        user.perfil.twitch_1 = self.cleaned_data['twitch_1']
        user.perfil.twitch_2 = self.cleaned_data['twitch_2']
        user.perfil.black_pan = self.cleaned_data['black_pan']
        user.perfil.telefono = self.cleaned_data['telefono']
        user.save()
        #user.Perfil.equipo = self.cleaned_data['equipo']
