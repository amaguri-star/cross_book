from django.urls import include, path   # includeを追加
from django.views.generic import TemplateView   # 追加
from cross_book import views

urlpatterns = [
    path('', views.home, name='home'),
]