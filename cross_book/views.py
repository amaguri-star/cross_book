from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django import forms
import json
from .forms import AddressForm, EditUserProfile, EditItemForm, CreateItemForm
from .models import *
from .decorators import *
from .api.viewsets import *
from django.db.models import Q
import pdb


def home(request):
    context = {}
    return render(request, 'cross_book/home.html', context)


@login_required
def my_page(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_item_list = user.item_set.order_by('-at_created')
    liked_item_list = Item.objects.filter(like__user=user).order_by('-at_created')
    context = {
        'user': user,
        'user_item_list': user_item_list,
        'liked_item_list': liked_item_list,
    }
    return render(request, 'cross_book/user-profile.html', context)


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
    return render(request, 'cross_book/edit-user-profile.html', context)


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
    return render(request, 'cross_book/address-form.html', context)


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
        labels=None,
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

    formset = image_form_set(queryset=Image.objects.none(), )
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
    requested = user.traderequest_set.filter(item=item).first()

    context = {
        'item': item,
        'user': user,
        'item_liked': item_liked,
        'item_images': item_images,
        'comments': comments,
        'requested': requested
    }

    return render(request, 'cross_book/item-detail.html', context)


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


@require_GET
def category_page(request, pk):
    if pk == 1:
        return redirect('home')
    category = get_object_or_404(Category, id=pk)
    items = Item.objects.filter(category=category)
    context = {'items': items, 'category': category}
    return render(request, 'cross_book/category-page.html', context)


@login_required
@require_POST
def create_room(request):
    req_user_id_for_item = request.POST.get('req_user_id_for_item')
    member1 = request.user
    member2 = get_object_or_404(User, pk=req_user_id_for_item)
    try:
        room = Room.objects.get(Q(roommember__member=member1) and Q(roommember__member=member2))
    except Room.DoesNotExist:
        room = Room.objects.create()
        RoomMember.objects.create(member=member1, room=room)
        RoomMember.objects.create(member=member2, room=room)
    return redirect('chat_room', room.id)


def get_chat_rooms(request):
    rooms = Room.objects.filter(roommember__member=request.user).order_by('-timestamp')
    other_room_member = []
    for room in rooms:
        other_member = RoomMember.objects.get(~Q(member=request.user), room=room.id)
        other_room_member.append(other_member)
    context = {'other_room_member': other_room_member}
    return context


@login_required
def chat_room_list(request):
    context = get_chat_rooms(request)
    return render(request, 'cross_book/chat-room-list.html', context)


@login_required
def chat_room(request, room_pk):
    context = get_chat_rooms(request)
    room_messages = get_object_or_404(Room, pk=room_pk).room_messages.all().order_by('created_at')
    other_member = RoomMember.objects.get(~Q(member=request.user), room_id=room_pk)
    context_new = {
        'room_pk': mark_safe(json.dumps(room_pk)),
        'username': mark_safe(json.dumps(request.user.username)),
        'room_messages': room_messages,
        'other_member_username': other_member.member.username,
    }
    context.update(context_new)
    return render(request, 'cross_book/chat-room-list.html', context)


@login_required
@require_POST
def likes(request):
    item = get_object_or_404(Item, id=request.POST.get('item_pk'))
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


@login_required
@require_POST
def request_item(request):
    user = request.user
    item = get_object_or_404(Item, id=request.POST.get('item_pk'))
    requested = False
    user_request = TradeRequest.objects.filter(user=user, item=item).first()

    if user_request:
        user_request.delete()
    else:
        tran_req = TradeRequest.objects.create(user=user, item=item)
        requested = True

    context = {
        'requested': requested,
    }

    if request.is_ajax():
        return JsonResponse(context)


@login_required
def view_item_trade_requests(request, pk):
    user = request.user
    item = get_object_or_404(Item, id=pk)
    requests_for_item = TradeRequest.objects.filter(item=item, item__user=user)
    context = {'requests_for_item': requests_for_item, 'item_pk': item.id}
    return render(request, 'cross_book/trade-request.html', context)


@login_required
@require_POST
def start_trade(request, pk):
    trade = Trade.objects.create()
    req_user_for_item = get_object_or_404(User, id=request.POST.get('trade_request_user_id'))
    traded_item = get_object_or_404(Item, id=pk)
    TradeInfo.objects.create(trader=request.user, trade=trade)
    TradeInfo.objects.create(trader=req_user_for_item, traded_item=traded_item, trade=trade)
    return redirect()


@login_required
@require_POST
def reject_trade_request(request, item_pk, trade_req_pk):
    trade_request = get_object_or_404(TradeRequest, id=trade_req_pk)
    trade_request.delete()
    return redirect('view_item_trade_requests', item_pk)


@require_GET
def search_item(request):
    q_word = request.GET.get('query')
    item_list = Item.objects.filter(
        Q(name__icontains=q_word) |
        Q(explanation__icontains=q_word) |
        Q(category__icontains=q_word))
    context = {
        'item_list': item_list,
        'item_count': item_list.count(),
        'q_word': q_word}
    return render(request, 'cross_book/search.html', context)