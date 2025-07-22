import stripe
import logging
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def charge_user(user, amount, stripe_token):
    """
    Makes a one-time payment for a user via Stripe.

    Args:
        user: the Django user (request.user)
        amount: amount to charge user (float or int)
        stripe_token: Stripe token returned by the frontend (Stripe.js)

    Returns:
        dict: {'success': True} if OK
              {'success': False, 'error': 'message'} else
    """
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    amount_cents = int(amount * 100)

    try:
        # create (or find) the Stripe client
        customer = stripe.Customer.create(
            name=user.first_name,
            email=user.email,
            source=stripe_token,
        )

        # debit
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount_cents,
            currency='eur',
            description=f"Renouvellement service okfacture.com pour {user.first_name}",
            metadata={
                'user_id': user.id,
                'username': user.first_name,
            }
        )

        # check if paid
        if charge.status == 'succeeded':
            return {'success': True, 'charge_id': charge.id, 'customer_id': customer.id}
        else:
            print("information reçu après l'echec du paiement: ", charge)
            logger.warning(f"Stripe charge not succeeded: {charge}")
            return {'success': False, 'error': "Le paiement n'a pas pu être confirmé."}

    except stripe.error.CardError as e:
        logger.error(f"CardError: {e}")
        return {'success': False, 'error': e.user_message}
    except stripe.error.StripeError as e:
        logger.error(f"StripeError: {e}")
        return {'success': False, 'error': 'Erreur avec le service de paiement. Veuillez réessayer.'}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {'success': False, 'error': 'Erreur interne. Veuillez réessayer plus tard.'}




def extend_access(user):
    now = timezone.now()
    access = user.useraccess
    if access.paid_until and access.paid_until > now:
        access.paid_until += timedelta(days=28)
    else:
        access.paid_until = now + timedelta(days=28)
    access.save()





def sendmail(request, **kwargs):
    usermail = kwargs['usermail']
    mailsubject = kwargs['mailsubject']
    template_html = kwargs['html_file']
    template_txt = kwargs['txt_file']


    info = {
        'username' : request.user.first_name,
        'email' : request.user.email,
        'useremail' : usermail,
        'protocol' : 'http://',
        'host' : request.META.get('HTTP_HOST'),
    }

    template_email = render_to_string(f'accounts/email/{template_html}', info)
    text_content = render_to_string(f"accounts/email/{template_txt}", info)

    email = EmailMultiAlternatives(
        mailsubject,
        text_content, 
        settings.EMAIL_HOST_USER, 
        [usermail],
    )
    email.attach_alternative(template_email, "text/html")
    email.fail_silently = False
    try:
        email.send()
        return "OK mail sent success"
    except Exception as e:
        print("envoie email echoue:", e)
        return "Fail to send mail"
