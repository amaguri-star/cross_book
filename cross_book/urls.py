from django.urls import include, path   # includeを追加
from django.views.generic import TemplateView   # 追加
from cross_book import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mypage/<int:pk>/', views.my_page, name='my_page'),
    path('mypage/<int:pk>/edit/', views.edit_user_profile, name='edit_user_profile'),
    path('set_address/', views.address_page, name='set_address'),
    path('sell/', views.sell_page, name="sell"),
    path('search/', views.search_item, name="search_item"),
    path('item/<int:pk>/', views.item_detail, name="item_detail"),
    path('item/<int:pk>/edit/', views.edit_item, name="edit_item"),
    path('item/<int:pk>/delete/', views.delete_item, name="delete_item"),
    path('item/<int:pk>/trade-requests/', views.view_item_trade_requests, name="view_item_trade_requests"),
    path('item/<int:item_pk>/trade-requests/<int:trade_req_pk>/delete/',
         views.reject_trade_request, name="reject_trade_request"),
    path('category/<int:pk>/', views.category_page, name="category_page"),
    path('create_room/', views.create_room, name="create_room"),
    path('chat/', views.chat_room_list, name="chat_room_list"),
    path('chat/<int:room_pk>/', views.chat_room, name="chat_room"),
    path('likes/', views.likes, name="likes"),
    path('trade_request/item/', views.request_item, name="trade_request_item"),
    path('start_trade/', views.start_trade, name="start_trade"),
]
