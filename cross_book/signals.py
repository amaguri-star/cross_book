from django.db.models.signals import post_save, pre_delete
from notifications.signals import notify
from django.dispatch import receiver, Signal
from django.utils import timezone
from .models import Address, User, Comment, Like, Notification, TradeRequest


@receiver(post_save, sender=User)
def create_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_address(sender, instance, **kwargs):
    instance.address.save()


@receiver(post_save, sender=Comment)
def send_comment_notify(sender, instance, created, *args, **kwargs):
    if created:
        Notification.objects.create(actor=instance.user, recipient=instance.item.user, type="comment",
                                    description="がコメントしました。", target=instance.item)


@receiver(post_save, sender=TradeRequest)
def send_transaction_request_notify(sender, instance, created, *args, **kwargs):
    if created:
        Notification.objects.create(actor=instance.user, recipient=instance.item.user, type="trade_request",
                                    description="が取引申請しました。", target=instance.item)


@receiver(post_save, sender=Like)
def send_like_notify(sender, instance, created, *args, **kwargs):
    if created:
        Notification.objects.create(actor=instance.user, recipient=instance.item.user, type="like",
                                    description="がいいねしました。", target=instance.item)
