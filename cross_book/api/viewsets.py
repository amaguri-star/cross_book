from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializersets import *
from cross_book.models import Notification


@api_view(['GET'])
def new_message_list(request):
    tasks = Notification.objects.filter(received=False)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

