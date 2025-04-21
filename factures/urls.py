from django.urls import path
from .views import auth, invoice


app_name="factures"

urlpatterns = [
    path("", auth.home, name="home"),
    path("dashboard", auth.dashboard, name="dashboard"),
    path("invoice/creation", invoice.create, name="create"),
    path("invoice/list", invoice.invoices, name="invoices"),
    path('invoice/<int:invoice_id>/add-item/', invoice.add_item_to_invoice, name='add_item'),
    path('invoice/<int:invoice_id>/detail/', invoice.invoice_detail, name='invoice_detail'),
    path('item/<int:item_id>/edit/', invoice.edit_item, name='edit_item'),
]