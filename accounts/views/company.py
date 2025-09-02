from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms.userform import CompanyForm


@login_required
def creation(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('factures:invoices')
    form = CompanyForm()
    context = {'form' : form}
    return render(request, 'accounts/company_creation.html', context)


def legal(request):
    return render(request, 'accounts/legal.html')