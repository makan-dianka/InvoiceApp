from django import forms
from factures.models.invoice import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['user', 'customer', 'title', 'number', 'issue_date', 'amount', 'description', 'is_paid']
        
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-select',  # Bootstrap style pour les <select>
            }),
            'customer': forms.Select(attrs={
                'class': 'form-select',  # Bootstrap style pour les <select>
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-select',
                'placeholder': 'Titre de la facture'
            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de facture'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optionnel)',
                'rows': 3
            }),
            'is_paid': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'user': "Utilisateur",
            'customer': "Client",
            'title': "Titre",
            'number': "Numéro de facture",
            'issue_date': "Date d'émission",
            'amount': "Montant",
            'description': "Description",
            'is_paid': "Payée ?",
        }