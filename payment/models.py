from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta



class UserAccess(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='useraccess')
    trial_start = models.DateTimeField(default=timezone.now)
    trial_end = models.DateTimeField()
    paid_until = models.DateTimeField(blank=True, null=True)

    def is_active(self):
        now = timezone.now()
        return now <= self.trial_end or (self.paid_until and now <= self.paid_until)

    @classmethod
    def create_for_user(cls, user):
        trial_end = timezone.now() + timedelta(days=15)
        return cls.objects.create(user=user, trial_end=trial_end)


    def __str__(self):
            return f"{self.user} — Actif : {self.is_active()}"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=250)
    charge_id = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return self.customer_id
