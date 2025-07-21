from django.urls import path
from . import views


app_name="payment"

urlpatterns = [
    path("", views.index, name="index"),
    path("challenge", views.payment_challenge, name="payment_challenge"),
]