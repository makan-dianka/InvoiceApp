# from django.contrib import admin
# from . models import invoice, user
# from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'amount', 'is_paid', 'issue_date')
    search_fields = ('number', 'user__email')
    list_filter = ('is_paid', 'issue_date')

# @admin.register(User)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'is_active', 'is_staff')
#     search_fields = ('email',)