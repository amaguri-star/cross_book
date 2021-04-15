from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from .models import Address, User, Comment, Request


@receiver(post_save, sender=User)
def create_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_address(sender, instance, **kwargs):
    instance.address.save()


@receiver(post_save, sender=Comment)
def send_notify(sender, instance, *args, **kwargs):
    print("send_notify")
    print(sender, instance.user.username, instance.item.user)
    notify.send(instance.user, recipient=instance.item.user, verb="comment-notify",
                description=str(instance.user.username) + "がコメントしました。")
