from django.urls import path
from .views import auth


app_name="factures"

urlpatterns = [
    path("register/", auth.register_view, name="regist"),
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),
]