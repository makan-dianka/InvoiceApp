from django.contrib import admin
from . models import Company

@admin.register(Company)
class ComapnyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'address', 'email', 'phone', 'siret', 'naf')
    search_fields = ('name', 'siret')
    list_filter = ('email',)
