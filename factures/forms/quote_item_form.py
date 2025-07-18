from django import forms
from factures.models.quote_item import QuoteItem

class QuoteItemForm(forms.ModelForm):
    class Meta:
        model = QuoteItem
        fields = ['unit', 'quantity', 'unit_price', 'description']
        widgets = {
            'unit': forms.Select(attrs={
                'class': 'form-select',
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