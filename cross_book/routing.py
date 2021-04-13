from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\d+)/$', consumer.ChatConsumer.as_asgi()),
    re_path(r'ws/item/(?P<room_name>\d+)/$', consumer.CommentConsumer.as_asgi()),
]