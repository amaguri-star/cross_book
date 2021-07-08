from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import settings_common, settings_dev

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('controll/', admin.site.urls),
    path('', include('cross_book.urls')),
    path('api/', include('cross_book.api.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings_common.MEDIA_URL, document_root=settings_dev.MEDIA_ROOT)

