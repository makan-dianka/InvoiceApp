from django.db import models
from .customer import Customer
from django.conf import settings


class Quote(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('refused', 'Refusé'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotes')
    number = models.CharField(max_length=50, blank=True)  # numéro unique **par utilisateur**
    issue_date = models.DateField()
    chantier = models.CharField(max_length=250, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    validity = models.IntegerField(default=15)
    rg_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # Ex: 5.00
    tva_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # Ex: 5.00

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'number')


    def total_ht(self):
        return sum(item.total_price for item in self.items.all())

    def tva_amount(self):
        return round(self.total_ht() * (self.tva_percentage / 100), 2)

    def total_ttc_tva(self):
        return round(self.total_ht() + self.tva_amount(), 2)

    def __str__(self):
        return self.number