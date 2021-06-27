from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import User, Item


# def unauthenticated_user(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('home')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func


def unauthorized_user(view_func):
    def wrapper_func(request, pk):
        if request.user != get_object_or_404(User, pk=pk):
            return redirect('home')
        else:
            return view_func(request, pk)
    return wrapper_func


def user_who_not_allowed_to_edit_or_delete(view_func):
    def wrapper_func(request, pk):
        item = get_object_or_404(Item, pk=pk)
        item_user = item.user
        if request.user != item_user:
            messages.error(request, "編集を許可されていません")
            return redirect('home')
        else:
            return view_func(request, pk)
    return wrapper_func
