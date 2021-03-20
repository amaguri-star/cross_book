from django.urls import include, path   # includeを追加
from django.views.generic import TemplateView   # 追加
from cross_book import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mypage/<int:pk>/', views.my_page, name='my_page'),
    path('mypage/<int:pk>/edit/', views.edit_user_profile, name='edit_user_profile'),
<<<<<<< HEAD
    path('set_address/', views.address_page, name='set_address')
=======
    path('set_address/', views.address_page, name='set_address'),
    path('sell', views.sell_page, name="sell")
>>>>>>> Item-model-and-sell-system
]