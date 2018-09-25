from django import forms
from . import models

class Inscripcion(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = []

class SignupForm(forms.Form):
    first_name = forms.ChoiceField(label='Plataforma ( pc o ps4 )', choices= ( ('pc', 'pc'), ('psn', 'psn'), ) ,widget=forms.Select(attrs={ 'class': 'input' ,'placeholder':('pc, ps4 (minusculas)'),'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=30, label='Usuario de Twitch (si tiene)', required=False, widget=forms.TextInput(attrs={ 'class': 'input' ,'placeholder':('Twitch user'),'autofocus': 'autofocus'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        #user.Perfil.equipo = self.cleaned_data['equipo']
