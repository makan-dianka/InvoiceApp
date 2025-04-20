from django.db import models
from .customer import Customer
from django.conf import settings


class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.TextField(blank=True) # chantier par exemple
    description = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    rg_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Ex: 5.00
    tva_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Ex: 5.00

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_ht(self):
        return sum(item.total_price for item in self.items.all())
    
    def rg_amount(self):
        return (self.total_ht() * self.rg_percentage) / 100
    
    def tva_amount(self):
        return (self.total_ht() * self.tva_percentage) / 100
    
    def total_ttc_rg(self):
        return self.total_ht() - self.rg_amount()

    def total_ttc_tva(self):
        return self.total_ht() + self.tva_amount() - self.rg_amount()

    def __str__(self):
        return f"Invoice {self.number} - {self.customer.name}"