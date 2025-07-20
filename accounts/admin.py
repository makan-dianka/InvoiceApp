from django.contrib import admin
from . models import Company, UserAccess, Payment

@admin.register(Company)
class ComapnyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'address', 'email', 'phone', 'siret', 'naf')
    search_fields = ('name', 'siret')
    list_filter = ('email',)


@admin.register(UserAccess)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'trial_start', 'trial_end', 'paid_until')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer_id', 'charge_id', 'amount', 'date')
