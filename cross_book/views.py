from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django import forms
import json
from .forms import AddressForm, EditUserProfile, EditItemForm, CreateItemForm
from .models import *
from .decorators import *
import pdb


def home(request):
    context = {}
    return render(request, 'cross_book/home.html', context)


def my_page(request, pk):
    user = get_object_or_404(User, pk=pk)
    all_items = Item.objects.all()
    items_of_user = user.item_set.all()
    length = items_of_user.count()
    users_item_first_image = []
    liked_list = []
    liked_item_first_image = []

    for item_of_user in items_of_user:
        users_item_first_image.append(item_of_user.image_set.all()[0])

    for item in all_items:
        liked = item.like_set.filter(user=user)
        if liked.exists():
            liked_list.append(item.id)
            liked_item_first_image.append(item.image_set.all()[0])

    context = {
        'user': user,
        'items_of_user': items_of_user,
        'length': length,
        'users_item_first_image': users_item_first_image,
        'liked_list': liked_list,
        'liked_item_first_image': liked_item_first_image
    }

    return render(request, 'cross_book/user_profile.html', context)


@login_required
@unauthorized_user
def edit_user_profile(request, pk):
    user = request.user
    form = EditUserProfile(instance=user)
    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールを変更しました。')
            return redirect('my_page', user.id)

    context = {'form': form}
    return render(request, 'cross_book/edit_user_profile.html', context)


@login_required
def address_page(request):
    user = request.user
    form = AddressForm(instance=request.user.address)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=user.address)
        if form.is_valid():
            form.save()
            messages.success(request, "配送先を変更しました。")
            return redirect('home')
    context = {'form': form}
    return render(request, 'cross_book/address_form.html', context)


@login_required
def sell_page(request):
    image_form_set = forms.inlineformset_factory(
        parent_model=Item,
        model=Image,
        fields=['image'],
        extra=3,
        max_num=3,
        can_delete=False,
        min_num=1,
        validate_min=True,
    )

    if request.method == "POST":
        form = CreateItemForm(request.POST)
        formset = image_form_set(request.POST, request.FILES, queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            images = formset.save(commit=False)
            for image in images:
                image.item = item
                image.save()
            messages.success(request, '商品を出品しました。')
            return redirect('my_page', request.user.id)
        else:
            return render(request, 'cross_book/sell.html', {'form': form, 'formset': formset})

    formset = image_form_set(queryset=Image.objects.none())
    form = CreateItemForm()
    context = {'form': form, 'formset': formset}
    return render(request, 'cross_book/sell.html', context)


@login_required
def item_detail(request, pk):
    user = request.user
    item = get_object_or_404(Item, pk=pk)
    comments = item.comment_set.all()
    item_liked = item.like_set.filter(user=user)
    item_images = item.image_set.all()
    thumbnail = item.image_set.all()[0]
    context = {
        'item': item,
        'user': user,
        'item_liked': item_liked,
        'item_images': item_images,
        'thumbnail': thumbnail,
        'comments': comments,
    }
    return render(request, 'cross_book/item_detail.html', context)


@login_required
@user_who_not_allowed_to_edit
def edit_item(request, pk):
    user = request.user
    item = get_object_or_404(Item, pk=pk)
    item_images = item.image_set.all()
    form = EditItemForm(instance=item)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "商品情報を編集しました。")
            return redirect('my_page', user.id)
    context = {'form': form, 'item_images': item_images}
    return render(request, 'cross_book/edit-item.html', context)


def category_page(request, pk):
    if pk == 1:
        return redirect('home')
    category = get_object_or_404(Category, id=pk)
    items = Item.objects.filter(category=category)
    item_first_images = []
    for item in items:
        image = item.image_set.all()[0]
        item_first_images.append(image)
    context = {'items': items, 'item_first_image': item_first_images, 'category': category}
    return render(request, 'cross_book/category_page.html', context)


@login_required
@require_POST
def create_room(request):
    item_num = request.POST.get('item_number')
    chatroom_user1 = request.user
    chatroom_user2 = get_object_or_404(Item, pk=item_num).user
    room = Room()
    room.save()
    room.users.add(chatroom_user1, chatroom_user2)
    return redirect('chat_room', room.id)


def __get_rooms_and_other_users(request):
    room_list = request.user.room_set.all()
    other_users_list = []
    for room in room_list:
        other_users_list.append(User.objects.filter(room=room).exclude(username=request.user.username)[0])
    context = {
        'room_list': room_list,
        'other_user_list': other_users_list,
    }
    return context


@login_required
def chat_room_list(request):
    context = __get_rooms_and_other_users(request)
    return render(request, 'cross_book/chat_room_list.html', context)


@login_required
def chat_room(request, room_pk):
    context_added = __get_rooms_and_other_users(request)
    room = get_object_or_404(Room, pk=room_pk)
    users = room.users.all()
    other_user = ""
    for user in users:
        if user != request.user:
            other_user = user
    room_messages = Message.objects.filter(room=room).order_by('created_at').all()
    context = {
        'room_pk': mark_safe(json.dumps(room_pk)),
        'username': mark_safe(json.dumps(request.user.username)),
        'room_messages': room_messages,
        'other_user': other_user,
    }
    context.update(context_added)
    return render(request, 'cross_book/chat_room_list.html', context)


@login_required
def likes(request):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=request.POST.get('item_id'))
        user = request.user
        liked = False
        like = Like.objects.filter(item=item, user=user)

        if like.exists():
            like.delete()
        else:
            like.create(item=item, user=user)
            liked = True

        context = {
            'item_id': item.id,
            'liked': liked,
            'count': item.like_set.count(),
        }

        if request.is_ajax():
            return JsonResponse(context)


