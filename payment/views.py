from django.shortcuts import render
from django.conf import settings

def index(request):
    return render(request, 'payment/index.html')



def payment_challenge(request):
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'payment/payment_challenge.html', context)
