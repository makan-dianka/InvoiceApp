from django.urls import path
from .views import auth, invoice_creation


app_name="factures"

urlpatterns = [
    path("", auth.home, name="home"),
    path("dashboard", auth.dashboard, name="dashboard"),
    path("invoice/creation", invoice_creation.invoice_creation, name="invoice_creation"),
]