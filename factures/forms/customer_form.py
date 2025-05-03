# forms/customer_form.py
from django import forms
from factures.models.customer import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'company', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email du client'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone du client'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'entreprise du client"}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "L'adresse du client"}),
        }


        labels = {
            'name': "Nom",
            'email': "Email",
            'phone': "Téléphone",
            'company': "Entreprise",
            'address': "Adresse",
        }