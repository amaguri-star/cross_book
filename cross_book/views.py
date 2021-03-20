from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddressForm, EditUserProfile
from .models import User


# Create your views here.
def home(request):
    context = {}
    return render(request, 'cross_book/home.html', context)


def my_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
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

