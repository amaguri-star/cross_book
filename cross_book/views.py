from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddressForm


# Create your views here.
def home(request):
    context = {}
    return render(request, 'cross_book/home.html', context)


def address_page(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=request.user.address)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddressForm(instance=request.user.address)
        context = {'form': form}
        return render(request, 'cross_book/address_form.html', context)
