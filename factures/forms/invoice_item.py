from django import forms
from factures.models.invoice_item import InvoiceItem
from factures.models.invoice import Invoice
from django.forms import inlineformset_factory



class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']



InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True
)