from django.contrib import admin
from . models import UserAccess, Payment


@admin.register(UserAccess)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'trial_start', 'trial_end', 'paid_until')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer_id', 'charge_id', 'amount', 'date')