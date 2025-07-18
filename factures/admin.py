from django.contrib import admin
from .models import Invoice, InvoiceItem, Customer
from factures.models.quote import Quote
from factures.models.quote_item import QuoteItem
from accounts.models import CustomUser


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'is_paid', 'issue_date')
    search_fields = ('number', 'user__email')
    list_filter = ('is_paid', 'issue_date')


@admin.register(InvoiceItem)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('description', 'quantity', 'unit_price', 'unit')



@admin.register(Customer)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')
    search_fields = ('email',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'status', 'issue_date')
    search_fields = ('customer',)


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'quantity', 'unit_price', 'unit')
