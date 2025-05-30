from django.urls import path
from .views import auth, invoice


app_name="factures"

urlpatterns = [
    path("", auth.home, name="home"),
    path("dashboard/", auth.dashboard, name="dashboard"),
    path("invoice/creation/", invoice.create, name="create"),
    path("invoice/list", invoice.invoices, name="invoices"),
    path('invoice/<int:invoice_id>/add-item/', invoice.add_item_to_invoice, name='add_item'),
    path('invoice/<int:invoice_id>/detail/', invoice.invoice_detail, name='invoice_detail'),
    path('item/<int:item_id>/edit/', invoice.edit_item, name='edit_item'),
    path('item/<int:item_id>/delete/', invoice.delete_item, name='delete_item'),

    path('invoice/<int:invoice_id>/edit/', invoice.edit, name='edit_invoice'),
    path('invoice/<int:invoice_id>/delete/', invoice.delete, name='delete_invoice'),


    path('invoice/<int:invoice_id>/pdf/', invoice.generate_invoice_pdf, name='invoice_pdf'),
    path('customer/creation/', invoice.create_customer, name='create_customer'),
    path('customer/list/', invoice.customer_list, name='customer_list'),

    path('customer/<int:customer_id>/edit/', invoice.edit_customer, name='edit_customer'),
]