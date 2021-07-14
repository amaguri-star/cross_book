import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_dev')

import django
django.setup()

from channels.auth import AuthMiddlewareStack
import channels.layers
from channels.routing import ProtocolTypeRouter, URLRouter
import cross_book.routing

channel_layer = channels.layers.get_channel_layer()
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            cross_book.routing.websocket_urlpatterns
        )
    )
})
