import stripe
import logging
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

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