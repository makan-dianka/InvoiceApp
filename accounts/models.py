from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Company(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='company', blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    siret = models.CharField(max_length=50)
    naf = models.CharField(max_length=50)

    def __str__(self):
        return self.name





class UserAccess(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='useraccess')
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=250)
    charge_id = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return self.customer_id