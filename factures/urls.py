from django.urls import path
from .views import auth


app_name="factures"

urlpatterns = [
    path("", auth.home, name="home"),
    path("dashboard", auth.dashboard, name="dashboard"),
]