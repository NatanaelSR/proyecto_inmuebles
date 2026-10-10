from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil, TIPO_USUARIO_CHOICES  # Importa desde .models, NO desde .forms

class RegistroUsuarioForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(
        choices=TIPO_USUARIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de Usuario'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Perfil.objects.create(
                usuario=user,
                tipo_usuario=self.cleaned_data['tipo_usuario']
            )
        return user