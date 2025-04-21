# views.py
from django.shortcuts import render, redirect, get_object_or_404
from factures.forms.invoice_form import InvoiceForm
from factures.models.invoice import Invoice
from factures.models.invoice_item import InvoiceItem
from factures.forms.invoice_item import InvoiceItemForm




def create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect("factures:invoices")  # à adapter selon ton URL
    else:
        form = InvoiceForm()
    return render(request, "factures/invoice_creation.html", {"form": form})



# continue ici demain 21/4/2025
def add_item_to_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            item.save()
            return redirect('factures:invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceItemForm()

    return render(request, 'factures/add_item.html', {
        'invoice': invoice,
        'form': form
    })




def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice_item = InvoiceItem.objects.get(invoice=invoice)
    return render(request, 'factures/invoice_detail.html', {'invoice': invoice, 'invoice_item': invoice_item})




def invoices(request):
    invoices = Invoice.objects.all()
    return render(request, "factures/invoice_list.html", {'invoices': invoices})