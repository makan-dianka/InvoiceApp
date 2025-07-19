from django.urls import path
from .views import auth, company


app_name="accounts"

urlpatterns = [
    path("register/", auth.register_view, name="register"),
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),
    path("companyCreation/", company.creation, name="company_creation"),

    path('mentions-legales/', company.legal, name='legal'),
]