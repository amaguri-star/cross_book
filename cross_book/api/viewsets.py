from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializersets import NotificationSerializer
from cross_book.models import Notification


@api_view(['GET'])
def new_message_list(request):
    notifications = Notification.objects.filter(new_message=True)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

