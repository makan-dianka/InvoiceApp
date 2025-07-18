from django.db import models
from .quote import Quote
from django.conf import settings


class QuoteItem(models.Model):
    UNIT = [
        ('m2', 'M²'),
        ('ml', 'ML'),
        ('u', 'Unité'),
        ('autre', 'Autre'),
    ]
    quote = models.ForeignKey(Quote, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, choices=UNIT, default='unité')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} - {self.total_price}€"