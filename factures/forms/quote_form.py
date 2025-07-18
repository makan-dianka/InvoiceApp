from django import forms
from factures.models.quote import Quote
from factures.models.customer import Customer

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['customer', 'issue_date', 'chantier', 'tva_percentage', 'status', 'validity']

        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select',
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

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'validity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'la valité du devis. ex: 10 jours'}),
        }

        labels = {
            'customer': "Client",
            'chantier': "Le chantier",
            'tva_percentage' : 'TVA',
            'issue_date': "Date d'émission",
            'status': "L'état",
            'validity' : 'Valable pour'
        }

        help_texts = {
            'tva_percentage': "Indiquez le pourcentage de TVA applicable (exemple : 5 pour 5%). À défault c'est 20%",
            'validity' : "Indiquez la validité, ex (10 pour 10 jours). À default c'est 15 jours"
        }




    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)