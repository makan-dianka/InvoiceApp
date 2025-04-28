from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404




from weasyprint import HTML




from factures.forms.invoice_item import InvoiceItemForm
from factures.models.invoice_item import InvoiceItem
from factures.forms.invoice_form import InvoiceForm
from factures.models.invoice import Invoice












#-------------------------------------
# ---->  START section invoice <------
#-------------------------------------
@login_required
def create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect("factures:invoices")
    else:
        form = InvoiceForm(user=request.user)
    return render(request, "factures/invoice_creation.html", {"form": form})



@login_required
def edit(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.user != request.user:
        raise Http404("Cette facture n'existe pas.")
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('factures:invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm(instance=invoice)

    return render(request, 'factures/invoice_edit.html', {'form': form, 'invoice': invoice})




@login_required
def delete(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.user != request.user:
        raise Http404("Cette facture n'existe pas.")
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, "Facture supprimée avec succès.")
        return redirect('factures:invoice_list')

    return render(request, 'factures/invoice_confirm_delete.html', {'invoice': invoice})



@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.user != request.user:
        raise Http404("Cette facture n'existe pas.")
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)
    return render(request, 'factures/invoice_detail.html', {'invoice': invoice, 'invoice_items': invoice_items})




@login_required
def invoices(request):
    invoices = Invoice.objects.filter(user=request.user)
    return render(request, "factures/invoice_list.html", {'invoices': invoices})




# ----> END section invoice <------
#----------------------------------
#
#
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#                                    
#--------------------------------------
#----> START section invoice item <----
#--------------------------------------
@login_required
def add_item_to_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.user != request.user:
        raise Http404("Facture non trouvée.")
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


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(InvoiceItem, id=item_id)
    invoice = item.invoice
    if invoice.user != request.user:
        raise Http404("Article non trouvé.")

    if request.method == 'POST':
        form = InvoiceItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('factures:invoice_detail', invoice_id=invoice.id)

    form = InvoiceItemForm(instance=item)

    return render(request, 'factures/edit_item.html', {
        'form': form,
        'invoice': invoice,
        'item': item
    })


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(InvoiceItem, id=item_id)
    invoice = item.invoice

    if invoice.user != request.user:
        raise Http404("Article non trouvé.")

    if request.method == 'POST':
        item.delete()
        return redirect('factures:invoice_detail', invoice_id=invoice.id)

    return render(request, 'factures/delete_item_confirm.html', {'item': item})

# ----> END section invoice item <------
#----------------------------------
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# ----> PDF Generation <------
#----------------------------------
@login_required
def generate_invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    if invoice.user != request.user:
        raise Http404("Cette facture n'existe pas.")
    template = get_template('factures/invoice_pdf.html')
    html_content = template.render({'invoice': invoice})

    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="Facture_{invoice.number}.pdf"'
    return response