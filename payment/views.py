from django.shortcuts import render, redirect
from django.conf import settings
from utils.payment import charge_user, extend_access
from django.contrib.auth.decorators import login_required
from . models import Payment
from django.utils import timezone

@login_required
def index(request):
    return render(request, 'payment/index.html')


@login_required
def payment_challenge(request):
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }

    if request.method == 'POST':
        stripe_token = request.POST.get('stripeToken')
        AMOUNT = 19.99
        result = charge_user(request.user, AMOUNT, stripe_token)
        if result['success']:
            extend_access(request.user)
            payment = Payment(user=request.user, date=timezone.now(), charge_id=result.get('charge_id'), amount=AMOUNT, customer_id=result.get('customer_id'))
            payment.save()
            return render(request, "payment/payment_success.html")
        else:
            context['message'] = result['error']
            return redirect('payment:payment_challenge')
    return render(request, 'payment/payment_challenge.html', context)