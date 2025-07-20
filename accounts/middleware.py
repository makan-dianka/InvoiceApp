from django.shortcuts import redirect
from django.urls import reverse


class UserAccessMiddleware:
    """
    Blocks access to inactive users
    except for public, payment and authentication pages.
    """

    EXEMPT_URL_NAMES = [
        'accounts:login', 'accounts:logout', 'accounts:register', 'accounts:legal', 'factures:home', 'admin:index'
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'useraccess') and not request.user.useraccess.is_active():
                if not any(request.path.startswith(reverse(name)) for name in self.EXEMPT_URL_NAMES):
                    return redirect('payment')
        return self.get_response(request)
