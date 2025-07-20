from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms.userform import CompanyForm
from datetime import timedelta
from django.utils import timezone


@login_required
def creation(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('factures:dashboard')
    form = CompanyForm()
    context = {'form' : form}
    return render(request, 'accounts/company_creation.html', context)


def legal(request):
    return render(request, 'accounts/legal.html')




def extend_access(user):
    now = timezone.now()
    access = user.useraccess
    if access.paid_until and access.paid_until > now:
        access.paid_until += timedelta(days=28)
    else:
        access.paid_until = now + timedelta(days=28)
    access.save()
