# views.py
from django.shortcuts import render, redirect
from factures.forms.invoice_form import InvoiceForm
from factures.forms.invoice_item import  InvoiceItemFormSet

def invoice_creation(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()

            formset.instance = invoice
            formset.save()

            return redirect("invoices:list")  # à adapter selon ton URL
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(request, "factures/invoice_creation.html", {"form": form, "formset": formset})
