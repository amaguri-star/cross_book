from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django import forms
from .forms import AddressForm, EditUserProfile, EditItemForm, CreateItemForm
from .models import User, Item, Image, Like


# Create your views here.
def home(request):
    context = {}
    return render(request, 'cross_book/home.html', context)


def my_page(request, pk):
    user = get_object_or_404(User, pk=pk)
    all_items = Item.objects.all()
    items_of_user = user.item_set.all()
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
        'users_item_first_image': users_item_first_image,
        'liked_list': liked_list,
        'liked_item_first_image': liked_item_first_image
        }

    return render(request, 'cross_book/user_profile.html', context)


def edit_user_profile(request, pk):
    if request.user == User.objects.get(id=pk):
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
    else:
        return redirect('home')


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


def sell_page(request):
    user = request.user
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
        item = form.save(commit=False)
        formset = image_form_set(
            request.POST, request.FILES,
            instance=item,
            queryset=Image.objects.none()
        )
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.user = user
            item.save()
            formset.save()
            messages.success(request, '商品を出品しました。')
            return redirect('my_page', request.user.id)
    else:
        formset = image_form_set(
            queryset=Image.objects.none()
        )
        form = CreateItemForm()
    context = {'form': form, 'formset': formset}
    return render(request, 'cross_book/sell.html', context)


def item_detail(request, pk):
    user = request.user
    item = get_object_or_404(Item, pk=pk)
    item_liked = item.like_set.filter(user=user)
    item_images = item.image_set.all()
    thumbnail = item.image_set.all()[0]
    context = {
        'item': item,
        'user': user,
        'item_liked': item_liked,
        'item_images': item_images,
        'thumbnail': thumbnail
    }
    return render(request, 'cross_book/item_detail.html', context)


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
