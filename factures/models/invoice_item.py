from . invoice import Invoice
from django.db import models


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.TextField()
    unit = models.CharField(max_length=10)  # ex: m2, u, ml
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return round(self.quantity * self.unit_price, 2)

    def __str__(self):
        return f"{self.description} - {self.total_price}€"