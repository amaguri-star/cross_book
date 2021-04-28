from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializersets import NotificationSerializer
from cross_book.models import Notification, Item
from django.core import serializers


@api_view(['GET'])
def new_notify_list(request):
    notifications = Notification.objects.filter(recipient=request.user, new_message=True)
    new_notify_count = notifications.count()
    user_image_url_list = []
    item_image_url_list = []
    if notifications.exists():
        for noti in notifications:
            noti.new_message = False
            item_obj = Item.objects.get(id=noti.target_object_id)
            item_image_url_list.append(item_obj.image_set.first().image.url)
            user_image_url = noti.actor.image.url
            user_image_url_list.append(user_image_url)
            noti.save()

    serializer = NotificationSerializer(notifications, many=True)
    context = {
        'new_notify_count': new_notify_count,
        'serializer_data': serializer.data,
        'user_image_url_list': user_image_url_list,
        'item_image_url_list': item_image_url_list,
    }
    return Response(context)


@api_view(['GET'])
def unread_notify_count(request):
    unread_obj = Notification.objects.filter(recipient=request.user, unread=True)
    unread_count = unread_obj.count()
    return Response({'unread_count': unread_count})


@api_view(['POST'])
def read_notify(request):
    unread_objs = Notification.objects.filter(recipient=request.user, unread=True)
    for obj in unread_objs:
        obj.unread = False
        obj.save()
    return JsonResponse('success', safe=False)
