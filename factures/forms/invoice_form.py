from django import forms
from factures.models.invoice import Invoice
from factures.models.customer import Customer

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'issue_date', 'chantier', 'tva_percentage', 'is_paid']

        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select', 'id' : 'customer-field',  # Bootstrap style pour les <select>
            }),
            'chantier': forms.TextInput(attrs={'class': 'form-control'}),
            'tva_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }, format='%Y-%m-%d'),

            'is_paid': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'customer': "Client",
            'chantier': "Le chantier",
            'tva_percentage' : 'TVA',
            'issue_date': "Date d'émission",
            'is_paid': "Payée ?",
        }

        help_texts = {
            'tva_percentage': "Indiquez le pourcentage de TVA applicable (exemple : 5 pour 5%). À défault c'est 20%",
        }




    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)