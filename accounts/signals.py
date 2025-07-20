from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserAccess

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_user_access(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'useraccess'):
        UserAccess.create_for_user(instance)