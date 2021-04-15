from django.db.models.signals import post_save
from notifications.signals import notify
from django.dispatch import receiver
from django.utils import timezone
from .models import Address, User, Comment, Request


@receiver(post_save, sender=User)
def create_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_address(sender, instance, **kwargs):
    instance.address.save()


@receiver(post_save, sender=Comment)
def send_comment_notify(sender, instance, *args, **kwargs):
    notify.send(instance.user, recipient=instance.item.user, action_object=instance.item, verb="comment-notify",
                description=str(instance.user.username) + "がコメントしました。",
                timestamp=timezone.now(), parent_id=instance.item.id)


@receiver(post_save, sender=Request)
def send_user_request_notify(sender, instance, *args, **kwargs):
    notify.send(instance.sender, recipient=instance.receiver_item.user, action=instance.receiver_item.id, verb="user-request-notify",
                description=str(instance.sender) + "が取引申請しました", timestamp=timezone.now(), parent_id=instance.receiver_item.id)
