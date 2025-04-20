from django import forms
from ..models import CustomUser
from django.contrib.auth.forms import (
                                    UserCreationForm,
                                    PasswordChangeForm,
                                    PasswordResetForm,
                                   )



class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Saisir un nouveau mot de passe'}), label="Mot de passe")
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'}), label="Confirmer mot de passe")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre prénom ici', 'required': 'required', 'type' : 'text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre nom ici', 'required': 'required', 'type' : 'text'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Saisir votre adresse-email ici', 'type': 'email', 'required': 'required'}),
        }

        help_texts = {
            'username': None,
        }

        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse email',
        }