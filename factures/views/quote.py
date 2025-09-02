from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404




from weasyprint import HTML




from factures.forms.quote_form import QuoteForm
from factures.forms.quote_item_form import QuoteItemForm



from factures.models.quote import Quote
from factures.models.quote_item import QuoteItem
from factures.models.customer import Customer
from accounts.models import Company
from factures import utils





#-------------------------------------
# ---->  START section devis <------
#-------------------------------------
@login_required
def quote(request):
    quotes = Quote.objects.filter(user=request.user)
    return render(request, "devis/quote_list.html", {'quotes': quotes})




@login_required
def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if quote.user != request.user:
        raise Http404("Cette facture n'existe pas.")
    quote_items = QuoteItem.objects.filter(quote=quote)
    return render(request, 'devis/quote_detail.html', {'quote': quote, 'quote_items': quote_items})





@login_required
def create(request):
    if request.method == "POST":
        form = QuoteForm(request.POST, user=request.user)
        if form.is_valid():
            quote_number = utils.generate_quote_number(request.user)
            quote = form.save(commit=False)
            quote.user = request.user
            quote.number = quote_number
            quote.save()
            return redirect("factures:quote_list")
    else:
        form = QuoteForm(user=request.user)
    return render(request, "devis/quote_create.html", {"form": form})




@login_required
def quote_edit(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if quote.user != request.user:
        raise Http404("Ce devis n'existe pas.")
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect('factures:quote_detail', quote_id=quote.id)
    else:
        form = QuoteForm(instance=quote)

    return render(request, 'devis/quote_edit.html', {'form': form, 'quote': quote})




@login_required
def add_item_to_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if quote.user != request.user:
        raise Http404("Devis non trouvée.")
    if request.method == 'POST':
        form = QuoteItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.quote = quote
            item.save()
            return redirect('factures:quote_detail', quote_id=quote.id)
    else:
        form = QuoteItemForm()

    return render(request, 'devis/quote_item_create.html', {
        'quote': quote,
        'form': form
    })



@login_required
def quote_edit_item(request, item_id):
    item = get_object_or_404(QuoteItem, id=item_id)
    quote = item.quote
    if quote.user != request.user:
        raise Http404("Article non trouvé.")

    if request.method == 'POST':
        form = QuoteItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('factures:quote_detail', quote_id=quote.id)

    form = QuoteItemForm(instance=item)

    return render(request, 'devis/quote_item_edit.html', {
        'form': form,
        'quote': quote,
        'item': item
    })



def quote_to_invoice(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id, user=request.user)
    invoice = utils.convert_quote_to_invoice(quote)
    quote.status = 'accepted'
    quote.save()
    return redirect('factures:invoice_detail', invoice_id=invoice.id)





# ----> PDF Generation <------
#----------------------------------
@login_required
def generate_quote_pdf(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    if quote.user != request.user:
        raise Http404("Ce Devis n'existe pas.")

    try:
        user_company = Company.objects.get(owner=request.user)
    except Company.DoesNotExist:
        return redirect("accounts:company_creation")

    template = get_template('devis/quote_pdf.html')
    html_content = template.render({'quote': quote, 'company': user_company})

    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="DEVIS_{quote.number}.pdf"'
    return response