from django.shortcuts import render



def home(request):
    return render(request, 'factures/home.html', {})


def dashboard(request):
    return render(request, 'factures/dashboard.html', {})
