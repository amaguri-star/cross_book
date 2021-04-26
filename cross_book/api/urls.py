from django.urls import include, path
from . import viewsets

urlpatterns = [
    path('unread-notify-count/', viewsets.unread_notify_count, name='unread_notify_count'),
    path('new-notify-list/', viewsets.new_notify_list, name='new-notify-list'),
    path('read-notify/', viewsets.read_notify, name='read-notify'),
]