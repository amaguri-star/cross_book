from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Address, User


@receiver(post_save, sender=User)
def create_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_address(sender, instance, **kwargs):
    instance.address.save()
