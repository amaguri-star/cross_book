from django.urls import include, path
from . import viewsets

urlpatterns = [
    path('new-notify-list/', viewsets.new_message_list, name='new-message-list'),
]