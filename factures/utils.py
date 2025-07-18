from django.db import transaction
from factures.models.invoice import Invoice
from factures.models.quote import Quote

def generate_invoice_number(user):
    """
    Generates the next invoice number for a given user.
    Guarantees uniqueness per user and incremental numbering.
    """
    with transaction.atomic():
        last_invoice = (
            Invoice.objects.select_for_update()
            .filter(user=user)
            .order_by('-id')
            .first()
        )
        if last_invoice and last_invoice.number:
            try:
                last_num = int(last_invoice.number.split('-')[-1])
            except ValueError:
                last_num = 0
        else:
            last_num = 0

        return f"FACT-{last_num+1:04d}"




def generate_quote_number(user):
    """
    Generates the next quote number for a given user.
    Guarantees uniqueness per user and incremental numbering.
    """
    with transaction.atomic():
        last_quote = (
            Quote.objects.select_for_update()
            .filter(user=user)
            .order_by('-id')
            .first()
        )
        if last_quote and last_quote.number:
            try:
                last_num = int(last_quote.number.split('-')[-1])
            except ValueError:
                last_num = 0
        else:
            last_num = 0

        return f"DEVIS-{last_num+1:04d}"