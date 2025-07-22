import stripe
import logging
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging


def log(logger, log_status, message):
    """function to log message for debugging

    Args:
        logger (str): logger
        log_status (str): log status (debug, warning or critical)
        message (str): message to log
    """

    l = logging.getLogger(logger)
    if log_status == 'info':
        l.info(message)
    if log_status == 'debug':
        l.debug(message)
    if log_status == 'warning':
        l.warning(message)
    if log_status == 'error':
        l.error(message)
    if log_status == 'exception':
        l.exception(message)
    if log_status == 'critical':
        l.critical(message)




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
            log('debug_log', 'debug', f"Stripe charge not succeeded: {charge}")
            return {'success': False, 'error': "Le paiement n'a pas pu être confirmé."}

    except stripe.error.CardError as e:
        log('debug_log', 'error', f"CardError: {e}")
        return {'success': False, 'error': e.user_message}
    except stripe.error.StripeError as e:
        log('debug_log', 'error', f"StripeError: {e}")
        return {'success': False, 'error': 'Erreur avec le service de paiement. Veuillez réessayer.'}
    except Exception as e:
        log('debug_log', 'exception', f"Unexpected error: {e}")
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
        log('debug_log', 'info', "OK mail sent success")
    except Exception as e:
        log('debug_log', 'exception', f"Fail to send mail: {e}")