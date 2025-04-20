# models/customer.py
from django.db import models
from django.conf import settings

class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=150)
    company = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name