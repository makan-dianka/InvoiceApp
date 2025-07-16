from django import forms
from factures.models.invoice_item import InvoiceItem

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['unit', 'quantity', 'unit_price', 'description']
        widgets = {
            'unit': forms.Select(attrs={
                'class': 'form-select',  # Bootstrap style pour les <select>
            }),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix unitaire'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
        labels = {
            'description': "Description",
            'quantity': "Quantité",
            'unit_price': "Prix unitaire",
            'unit': "Unit",
        }