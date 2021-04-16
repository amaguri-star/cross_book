from django.db.models.signals import post_save, pre_save
from notifications.signals import notify
from django.dispatch import receiver
from django.utils import timezone
from .models import Address, User, Comment, TransactionRequest, Like


@receiver(post_save, sender=User)
def create_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_address(sender, instance, **kwargs):
    instance.address.save()


# def send_user_request_notify(sender, instance, created, *args, **kwargs):
#     notify.send(instance.user, recipient=instance.item.user, verb="user-request-notify",
#                 target=instance.item, description="が取引申請しました", timestamp=timezone.now())
#
#
# pre_save.connect(send_user_request_notify, sender=TransactionRequest)


@receiver(post_save, sender=Comment)
def send_comment_notify(sender, instance, *args, **kwargs):
    notify.send(instance.user, recipient=instance.item.user, verb="comment-notify", target=instance.item,
                description="がコメントしました。", timestamp=timezone.now())


@receiver(post_save, sender=Like)
def send_user_request_notify(sender, instance, *args, **kwargs):
    notify.send(instance.user, recipient=instance.item.user, verb="user-like-notify", target=instance.item,
                description="がいいねしました", timestamp=timezone.now())
