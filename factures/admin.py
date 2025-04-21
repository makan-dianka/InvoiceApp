from django.contrib import admin
from .models import Invoice, InvoiceItem, Customer
from accounts.models import CustomUser


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'amount', 'is_paid', 'issue_date')
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