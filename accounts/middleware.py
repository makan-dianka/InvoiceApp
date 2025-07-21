from django.shortcuts import redirect
from django.urls import reverse


class UserAccessMiddleware:
    """
    Blocks access to inactive users
    except for public, payment and authentication pages.
    """

    EXEMPT_PATHS = [
        reverse('accounts:login'),
        reverse('accounts:logout'),
        reverse('accounts:register'),
        reverse('accounts:legal'),
        reverse('factures:home'),
        reverse('payment:index'),
        reverse('payment:payment_challenge'),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'useraccess') and not request.user.useraccess.is_active():
                if request.path.startswith('/admin/'):
                    return self.get_response(request)
                if request.path not in self.EXEMPT_PATHS:
                    # print(f"Redirection: {request.path} n'est pas exempté")
                    return redirect('payment:index')
        return self.get_response(request)
