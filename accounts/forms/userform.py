from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
                                    UserCreationForm,
                                    PasswordChangeForm,
                                    PasswordResetForm,
                                   )



class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Saisir un nouveau mot de passe'}), label="Mot de passe")
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'}), label="Confirmer mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre nom d\'utilisateur ici'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre adresse-email ici'}),
        }

        help_texts = {
            'username': None,
        }